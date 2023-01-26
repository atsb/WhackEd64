#!/usr/bin/env python
#coding=utf8

from whacked64.ui import windows

import whacked64.utils as utils
import whacked64.config as config

import wx
import time
import random


class StatePreviewDialog(windows.StatePreviewDialogBase):
    """
    This dialog displays an animated preview of a state.
    """

    TICK_INTERVAL = 1000 / 35

    def __init__(self, parent):
        windows.StatePreviewDialogBase.__init__(self, parent)

        self.patch = None
        self.pwads = None

        # Thing for sound references.
        self.ref_thing_index = None
        self.ref_thing = None

        self.first_state_index = -1
        self.state_index = -1

        # Precise timer data.
        self.timer_prev = 0
        self.elapsed = 0
        self.ticks = 0

        self.Sprite.set_baseline_factor(0.85)
        self.Sprite.set_scale(2)

        self.StateInfo.SetFont(config.FONT_MONOSPACED_BOLD)
        self.StateAction.SetFont(config.FONT_MONOSPACED_BOLD)
        self.StateSound.SetFont(config.FONT_MONOSPACED_BOLD)
        self.SpawnSound.SetFont(config.FONT_MONOSPACED_BOLD)

        self.SetEscapeId(windows.PREVIEW_CLOSE)

        self.Bind(wx.EVT_CHAR_HOOK, self.key_hook)

    def update(self, pwads):
        self.pwads = pwads

        self.Sprite.set_source(self.pwads)
        self.Sprite.Refresh()

    def key_hook(self, event):
        """
        Intercepts all key presses.
        """

        # Tilde restarts the animation from the state this dialog was called with.
        if event.GetKeyCode() == 96:
            self.begin_playback(self.first_state_index)
            self.anim_start()
        else:
            event.Skip()

    def begin_playback(self, state_index):
        """
        Starts playbackl from a state. Takes care of moving voer 0 duration starting states.
        """

        self.set_state(state_index)
        while self.ticks == 0:
            state = self.patch.states[self.state_index]
            self.set_state(state['nextState'])

    def prepare(self, pwads, patch, state_index, thing_index=None):
        """
        Used to prepare a new animation to preview.
        """

        self.pwads = pwads
        self.patch = patch
        self.first_state_index = state_index

        self.ref_thing_index = thing_index
        if thing_index is not None:
            self.ref_thing = patch.things[thing_index]
        else:
            self.ref_thing = None

        self.Sprite.set_source(pwads)
        self.set_title()
        self.begin_playback(state_index)

    def set_title(self):
        if self.ref_thing_index is not None:
            title = 'Preview - {}'.format(self.patch.things.names[self.ref_thing_index])
        else:
            title = 'Preview'

        self.SetLabel(title)

    def activate(self, event):
        """
        Window activation event.
        """

        self.anim_start()

    def anim_start(self):
        """
        Starts animation playback from the current state.
        """

        self.timer_prev = time.time()
        self.Timer.Start(1)

    def anim_stop(self):
        """
        Stops animation playback.
        """

        self.Timer.Stop()

    def set_state(self, state_index):
        """
        Sets a new state index.
        """

        if state_index <= 1 or state_index >= len(self.patch.states):
            self.ticks = -1
            self.anim_stop()
            return

        state = self.patch.states[state_index]
        sprite_index = state['sprite']
        sprite_name = self.patch.sprite_names[sprite_index]
        sprite_frame = state['spriteFrame'] & 0x3FFF

        self.Sprite.show_sprite(sprite_name, sprite_frame)

        self.StateIndex.SetLabel(str(state_index))
        self.StateInfo.SetLabel('{}{}'.format(sprite_name, chr(65 + sprite_frame)))

        action_label = ''

        # Play any state-related sound.
        if state['action'] is not None:

            # Support for RandomJump action that takes parameters to jump to a random next state.
            if state['action'] == 'RandomJump' and random.randint(0, 255) < state['unused2']:
                self.set_state(state['unused1'])
                return

            action_label = state['action']

            action_name = state['action']
            action = self.patch.engine.actions[action_name]

            sound_label = ''
            sound_index = None

            spawn_sound_label = ''
            spawn_sound_index = None

            if 'sound' in action:
                parts = action['sound'].split(':')
                if len(parts) != 2:
                    raise Exception('Invalid sound for action {}'.format(action_name))

                if parts[0] == 'sound':
                    sound_index = int(parts[1])

                elif parts[0] == 'thing':
                    if self.ref_thing_index is not None:
                        sound_index = self.ref_thing[parts[1]]
                    else:
                        sound_label = '{}:{}'.format(parts[0], parts[1])

                elif parts[0] == 'state':
                    sound_index = state[parts[1]]

            # Action spawns a thing.
            if 'spawns' in action:
                thing = self.patch.things[action['spawns']]
                spawn_sound_index = thing['soundAlert']

            # Playback sounds for this action. Any specific sound overrides a spawned thing sound.
            if sound_index is not None:
                utils.sound_play(self.patch.sound_names[sound_index - 1], self.pwads)
                sound_label = self.patch.sound_names[sound_index - 1]
            elif spawn_sound_index is not None:
                utils.sound_play(self.patch.sound_names[spawn_sound_index - 1], self.pwads)
                spawn_sound_label = self.patch.sound_names[spawn_sound_index - 1]

            self.SpawnSound.SetLabel(spawn_sound_label.upper())
            self.StateSound.SetLabel(sound_label.upper())

        self.StateAction.SetLabel(action_label)

        self.state_index = state_index
        self.ticks = state['duration']

    def timer(self, event):
        """
        Timer event.
        """

        # Figure out the exact time that has passed since the last call to this event.
        # The Timer control may not be precise enough in it's timing, so we rely on Python's time.time() for
        # more accurate time accounting.
        self.elapsed += (time.time() - self.timer_prev) * 1000
        self.timer_prev = time.time()

        # If too much time has passed since the previous event, just do a single tick to prevent needless updating.
        if self.elapsed > 3000:
            self.elapsed = self.TICK_INTERVAL

        # Keep ticking until all elapsed time has been ticked through.
        while self.elapsed >= self.TICK_INTERVAL:
            self.elapsed -= self.TICK_INTERVAL
            self.advance_tick()

    def advance_tick(self):
        """
        Advances the animation a single tick.
        """

        self.ticks -= 1
        while self.ticks == 0:
            state = self.patch.states[self.state_index]
            self.set_state(state['nextState'])

    def close(self, event):
        """
        Close event.
        """

        self.anim_stop()
        self.EndModal(0)
