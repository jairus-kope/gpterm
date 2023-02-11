import os
import sys
import readline
import cmd
import enum
from gpterm.enums import ThemeMode, VoiceStop, GptModel
from gpterm.config import Config


class ShellHandler(cmd.Cmd):
    intro = None
    prompt = "> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.gpterm = None
        self.loop_index = 0
        self._set_completion_delims()
        self._setup_command_handlers()

    def _set_completion_delims(self):
        delims = readline.get_completer_delims().replace('/', '').replace('-', '')
        readline.set_completer_delims(delims)

    def _setup_command_handlers(self):
        self.cmd_handlers = {
            "/help": self.handle_help,
            "/exit": self.handle_exit,
            "/abort": self.handle_exit,
            "/save": self.handle_save,
            "/reset": self.handle_reset,
            "/context": self.handle_context,
            "/theme": self.handle_theme,
            "/code": self.handle_code,
            "/advanced": self.handle_advanced,
            "/voice": self.handle_voice,
            "/voice-name": self.handle_voice_name,
            "/voice-over": self.handle_voice_over,
            "/voice-stop": self.handle_voice_stop,
            "/model": self.handle_model,
            "/temperature": self.handle_temperature,
            "/block": self.handle_block,
            "/image": self.handle_image,
            "/image-size": self.handle_image_size,
            "/image-view": self.handle_image_view,
            "/image-store": self.handle_image_store,
            "//code_initial": self.handle_code_initial,
        }

    def preloop(self) -> None:
        if self.loop_index == 0:
            self.print_intro()
            if self.gpterm.cfg.use_code_format:
                self.onecmd("//code_initial")
        self.loop_index = 1

    def print_intro(self):
        self.stdout.write(str(self.gpterm.gpterm_intro) + "\n")

    def set_gpt_terminal(self, gpt_terminal):
        self.gpterm = gpt_terminal

    def set_shell_prompt(self, shell_prompt):
        self.prompt = shell_prompt

    def default(self, line):
        if not self.handle_command(line):
            self.gpterm.submit_prompt(line)

    def do_shell(self, line):
        os.system(line)

    def get_multiline(self, instruction="Enter multi-line input"):
        """
        Prompt for multi-line input
        """
        print(f"{instruction}. End with a '.' on a line by itself.")
        lines = []
        while True:
            line = input()
            if line == '.':
                break
            lines.append(line)
        prompt = '\n'.join(lines)
        return prompt

    def emptyline(self):
        return

    def completenames(self, text, *ignored):  # a bit of a hack
        return self.get_command_completions(text)

    def get_command_completions(self, text):
        gpterm_commands = self.gpterm.get_commands(advanced=self.gpterm.cfg.display_advanced)
        gpterm_commands = list(gpterm_commands.keys()) + ['shell']
        if text:
            return [command for command in gpterm_commands if command.startswith(text)]
        else:
            return gpterm_commands

    def do_help(self, line):
        self.default(line)

    def get_voice_name_help(self):
        self.gpterm.console.print(f"Available Voices:")
        self.onecmd("!say -v '?'")
        msg = "Command format: /voice-name <speaker_name>"
        return msg

    def handle_exit(self, _):
        sys.exit(0)

    def handle_help(self, _):
        self.print_intro()
        msg = self.help_message()
        return msg

    def handle_save(self, _):
        self.gpterm.cfg.save()
        msg = "Settings saved to disk"
        return msg

    def handle_reset(self, _):
        self.gpterm.reset_context(prompt="", submit=True)
        msg = f"[bold red]*** Chat context reset ***[/]"
        return msg

    def handle_context(self, _):
        self.gpterm.print_info(f"{self.gpterm.conversation_formatted}")

    def handle_theme(self, _):
        theme = self.gpterm.toggle_theme()
        msg = f"Color theme = {'dark' if theme == ThemeMode.dark else 'light'}"
        return msg

    def handle_code(self, _):
        on = self.gpterm.toggle_code()
        msg = self.handle_reset(_)
        msg += f"\nCode format = {on}"
        return msg

    def handle_advanced(self, _):
        on = self.gpterm.toggle_advanced()
        msg = f"Display advanced commands = {on}"
        return msg

    def handle_voice(self, _):
        on = self.gpterm.toggle_voice()
        msg = f"Voice = {on}"
        return msg

    def handle_voice_name(self, command):
        msg = ""
        if len(command) == 2:
            try:
                rc = os.system(f"say -v {command[1]} ''")
                if rc == 0:
                    self.gpterm.cfg.voice_name = command[1]
                    msg = f"Voice name set to '{command[1]}'"
            except:
                pass
        if not msg:
            msg = self.get_voice_name_help()
        return msg

    def handle_voice_over(self, _):
        on = self.gpterm.toggle_voice_over()
        msg = f"voice over = {on}"
        return msg

    def handle_voice_stop(self, _):
        voice_stop = self.gpterm.toggle_voice_stop()
        msg = f"voice stop = "
        msg += "period" if voice_stop == VoiceStop.period else "newline"
        return msg

    def handle_model(self, command):
        models = [e.name for e in GptModel]
        msg = f"Command format: /model <{'|'.join(models)}>"
        if len(command) == 2 and command[1] in models:
            self.gpterm.cfg.model = GptModel[command[1]]
            self.gpterm.calc_max_tokens()
            self.gpterm.update_shell_prompt()
            msg = f"GPT-3 Model set to '{self.gpterm.cfg.model.name}'"
        return msg

    def handle_temperature(self, command):
        msg = "Command format: /temperature <value between 0-1>"
        if len(command) == 2:
            try:
                val = float(command[1])
                if 0 <= val <= 1:
                    self.gpterm.cfg.temperature = val
                    msg = f"Model temperature set to {self.gpterm.cfg.temperature}"
            except ValueError:
                pass
        return msg

    def handle_block(self, _):
        prompt = self.get_multiline()
        if prompt:
            self.gpterm.submit_prompt(prompt)

    def handle_image(self, _):
        prompt = self.get_multiline(instruction="Enter multi-line input to describe image")
        if prompt:
            self.gpterm.submit_image_gen_request(prompt=prompt)

    def handle_image_size(self, command):
        msg = "Command format: /image-size <256|512|1024>"
        if len(command) == 2:
            try:
                val = int(command[1])
                if val in [256, 512, 1024]:
                    self.gpterm.cfg.image_size = val
                    msg = f"Generated image size set to: {self.gpterm.cfg.image_size} x {self.gpterm.cfg.image_size}"
            except ValueError:
                pass
        return msg

    def handle_image_view(self, _):
        on = self.gpterm.toggle_image_view()
        msg = f"image view = {on}"
        return msg

    def handle_image_store(self, command):
        msg = f"Images store path: {self.gpterm.cfg.image_store}\n"
        msg += f"Command format: /image-store [<path>|reset]"
        if len(command) == 2:
            if command[1] == "reset":
                new_path = Config.DEFAULT_IMAGE_STORE_PATH
            else:
                new_path = os.path.abspath(os.path.expanduser(os.path.expandvars(command[1])))
            msg = f"Failed to set store to '{new_path}'. "
            try:
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if os.path.exists(new_path):
                    if os.access(new_path, os.W_OK):
                        self.gpterm.cfg.image_store = new_path
                        msg = f"Images store path: {self.gpterm.cfg.image_store}"
                    else:
                        msg += "Path is not writable"
                else:
                    msg += "Failed to create path"
            except Exception as e:
                msg += f"with error: {e}"
        return msg

    def handle_code_initial(self, _):
        self.gpterm.apply_code_format_directive()

    def handle_command(self, command):
        if not command:
            return False

        if '\n' in command:  # shouldn't happen
            return False

        command = command.strip().split()
        if not command[0].startswith('/'):
            return False

        if command[0] not in self.cmd_handlers:
            return False

        # if len(command) > 2:
        #     self.gpterm.print_info(msg)
        #     return True
        if len(command) > 1:
            all_commands = self.gpterm.get_commands(advanced=True)
            nargs_commands = {key for key in all_commands if all_commands[key].nargs > 0}
            if command[0] not in nargs_commands:
                self.gpterm.print_info(f"Command format: {command[0]}")
                return True

        msg = self.cmd_handlers[command[0]](command)
        if msg:
            self.gpterm.print_info(msg)
        return True

    def help_message(self):
        advanced = self.gpterm.cfg.display_advanced
        msg = f"[{self.gpterm.colors.cinfo}]GPTerm commands:[/]\n"
        gpterm_commands = self.gpterm.get_commands(advanced=advanced)
        key_len = len(max(gpterm_commands.keys(), key=len)) + 1
        for k, v in gpterm_commands.items():
            if v.setting is None:
                state = "\t"
                tab = "\t"
            elif isinstance(v.setting, enum.Enum):
                val_text = v.setting.name
                state = f"= [{self.gpterm.colors.cinfo}]{val_text}[/]"
                tab = '\t' if len(val_text) < 8 else ''
            else:
                val_text = str(v.setting)
                state = f"= {val_text}"
                tab = '\t' if len(val_text) < 8 else ''
            msg += f"{k:<{key_len}} {state}\t{tab} # {v.description}\n"
        if advanced:
            color = "#ff77ff" if self.gpterm.cfg.color_theme == ThemeMode.dark else "#ff00ff"
            msg += "!<shell_command>\t\t # Run a shell command\n"
            msg += f"[{color}]cmd+k[/]\t\t\t\t # Clear the screen\n"
            msg += f"[{color}]ctrl+c[/]\t\t\t\t # Exit GPTerm or abort a GPT response\n"
        return msg.rstrip()
