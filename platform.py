# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from platformio.managers.platform import PlatformBase


class Nordicnrf52Platform(PlatformBase):

    def is_embedded(self):
        return True

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug['tools'] = {}

        # J-Link
        if "jlink" not in debug['tools']:
            debug['tools']['jlink'] = {
                "server": {
                    "package": "tool-openocd",
                    "executable": "bin/openocd",
                    "arguments": [
                        "-f", "scripts/interface/jlink.cfg",
                        "-f", "scripts/target/nrf52.cfg"
                    ]
                }
            }

        # ST-Link
        if "stlink" not in debug['tools']:
            debug['tools']['stlink'] = {
                "server": {
                    "package": "tool-openocd",
                    "executable": "bin/openocd",
                    "arguments": [
                        "-f", "scripts/interface/stlink.cfg",
                        "-f", "scripts/target/nrf52.cfg"
                    ]
                }
            }

        # BlackMagic Probe
        if "blackmagic" not in debug['tools']:
            debug['tools']['blackmagic'] = {
                "hwids": [["0x1d50", "0x6018"]],
                "require_debug_port": True
            }

        board.manifest['debug'] = debug
        return board
