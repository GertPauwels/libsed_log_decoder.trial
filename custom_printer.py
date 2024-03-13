#!/usr/bin/python3
# Copyright 2023 pauwels.tech
# SPDX-License-Identifier: BSD-3-Clause
# For inquiries, please contact: Gert.Pauwels@pauwels.tech

# Python 3.6 or later is the recommended version to run this script.

# The script adheres to PEP 8 style guidelines, including proper indentation, consistent spacing,
#    and the use of appropriate naming conventions.

# Python standard libraries, which are released under the Python Software Foundation License (PSF License). 
#   The PSF License is an open source license that is compatible with the GNU General Public License (GPL).
import re               # Provides support for regular expressions (pattern matching) and text manipulation
import sys              # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
from io import open     # Importing the open function explicitly
# The colorama module is released under BSD 3-Clause License. The BSD 3-Clause License is a permissive open source license 
#   that allows for the modification, distribution, and use of the software, with certain conditions.
from colorama import Fore, Style  # pip install colorama


# Set the script version
VERSION = "1.0.0"
# Define the minimum required Python version
MIN_PYTHON_VERSION = (3, 6)

class CustomPrinter:
    """
    Custom printer class for printing colored text to console and optionally to HTML file.
    """

    def __init__(self, color=True, write_to_html=False, html_file_name=None, end_line=True):
        """
        Initialize CustomPrinter with specified settings.

        Args:
            color (bool, optional): Flag to enable or disable ANSI color codes. Defaults to True.
            write_to_html (bool, optional): Flag to enable or disable writing to HTML file. Defaults to False.
            html_file_name (str, optional): Name of the HTML file. Defaults to None.
            end_line (bool, optional): Flag to append a newline character at the end of each print. Defaults to True.

        """
        self.color = color
        self.write_to_html = write_to_html
        self.html_file_name = html_file_name
        self.use_block = False
        self.second_part = False
        self.add_div = False
        self.message_color_dark = True  # Start with the dark color
        self.block_characters = {
            'start': '/',
            'mid': '|',
            'end': '\\',
            'none_second_part': '',
            'none': ''
        }
        self.end_line = end_line
        if self.write_to_html:
            self.write_html_header()
            self.write_html_buttons(html_file_name)

    def __del__(self):
        """
        Destructor to ensure proper cleanup by writing HTML footer if needed.
        """
        if self.write_to_html:
            self.write_html_footer()

    def print_and_write_colored(self, text, color, block_type, end_line):
        """
        Prints colored text and writes it to the file if required.

        Args:
            text (str): Text to be printed.
            color (str): ANSI color code.
            block_type (str): Type of block (start, mid, end).
        """
        if self.write_to_html:
            self.write_to_html_file(text, block_type, end_line)
        
        if self.use_block:
            if block_type == 'start':
                block_character = self.block_characters['start']
            elif block_type == 'mid':
                block_character = self.block_characters['mid']
            elif block_type == 'end':
                block_character = self.block_characters['end']
            elif block_type == 'none_second_part':
                block_character = self.block_characters['none_second_part']
            elif block_type == 'none':
                block_character = self.block_characters['none']
                
            else:
                block_character = self.block_characters['none']
        else:
            block_character = ''
        # Print to console with ANSI colors if enabled
        if self.color:
            print(f"{block_character}{text}", end='' if not end_line else '\n')
        else:
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            stripped_text = ansi_escape.sub('', text)
            print(stripped_text, end='' if not end_line else '\n')

    def print(self, text, color=Fore.WHITE, block_type='mid', end_line=None):
        """
        Prints colored text to console and writes it to HTML file if required.

        Args:
            text (str): Text to be printed.
            color (str, optional): ANSI color code. Defaults to Fore.WHITE.
            block_type (str, optional): Type of block (start, mid, end). Defaults to 'mid'.
            end_line (bool, optional): Flag to append a newline character at the end of print. Defaults to None,
                in which case it uses the value set during object initialization.
        """
        if end_line is None:
            end_line = self.end_line

        if self.color:
            self.print_and_write_colored(text, color, block_type, end_line)
        else:
            self.print_and_write_colored(text, "", block_type, end_line)

    def set_color(self, color):
        """
        Set the flag to enable or disable ANSI color codes.

        Args:
            color (bool): Flag to enable or disable ANSI color codes.
        """
        self.color = color

    def set_write_to_html(self, write_to_html):
        """
        Set the flag to enable or disable writing to HTML file.

        Args:
            write_to_html (bool): Flag to enable or disable writing to HTML file.
        """
        self.write_to_html = write_to_html

    def set_html_file_name(self, html_file_name):
        """
        Set the name of the HTML file.

        Args:
            html_file_name (str): Name of the HTML file.
        """
        self.html_file_name = html_file_name

    def set_use_block(self, use_block):
        """
        Set the flag to enable or disable using block characters.

        Args:
            use_block (bool): Flag to enable or disable using block characters.
        """
        self.use_block = use_block

    def set_block_characters(self, start_char, mid_char, end_char):
        """
        Set the block characters.

        Args:
            start_char (str): Character for start block.
            mid_char (str): Character for mid block.
            end_char (str): Character for end block.
        """
        self.block_characters['start'] = start_char
        self.block_characters['mid'] = mid_char
        self.block_characters['end'] = end_char
 
    def write_html_header(self):
        """
        Writes the HTML header to the file.
        """
        header = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>sedcli_parser</title>
<style>
    p {
      white-space: pre-wrap;
    }

  .collapsible {
    font-family: "Courier New", Courier, monospace;
    cursor: pointer;
    user-select: none;
    border: none;
    outline: none;
    font-size: 14px;
    transition: 0.4s; 
    padding: 0;
    margin: 0;
    margin-left: 10px; /* Adjust this value as needed */
    float: left;
    position: relative; /* To position the ::before pseudo-element */
    padding-left: 10px;
  }

  .collapsible::before {
    content: "+";
    width: 14px; /* Fixed width */
    display: inline-block; /* To allow for setting width */
    position: absolute; /* Positioning relative to the parent */
    left: 0; /* Align to the left of the parent */
  }

  .active::before {
    content: "-";
  }

  .message {
    display: flex;
    flex-direction: column;
  }

  .message_dark {
    display: flex;
    flex-direction: column;
    background-color: black;
    color: white;
}

  .message_light {
    display: flex;
    flex-direction: column;
    background-color: rgb(22, 22, 22);
    color: white;
}

  .content {
    display: none;
    overflow: hidden;

    font-size: 14px;
    font-family: "Courier New", Courier, monospace;
    margin-left: 10px;
    padding-left: 0px;
  }

  .content p {
    margin: 0;
    text-indent: 20px; /* Indentation for paragraphs */
    margin-top: 0; /* Remove spacing before paragraphs */
    margin-bottom: 0; /* Remove spacing after paragraphs */
  }

  .button-container {
    margin-bottom: 10px;
  }
</style>
</head>
<body>
"""
        with open(self.html_file_name, 'w') as file:
            file.write(header)

    def write_html_buttons(self, filename):
        buttons = f"<div class=\"button-container\">\n  <button onclick=\"collapseAll()\">Collapse All</button>\n  <button onclick=\"expandAll()\">Expand All</button>\n  {filename}\n</div>\n"
        with open(self.html_file_name, 'a') as file:
            file.write(buttons)

    def write_html_footer(self):
        """
        Writes the HTML footer to the file.
        """
        footer = """
<script>
function collapseAll() {
  var coll = document.getElementsByClassName("collapsible");
  for (var i = 0; i < coll.length; i++) {
    var content = coll[i].nextElementSibling;
    content.style.display = "none";
    coll[i].classList.remove("active");
  }
}

function expandAll() {
  var coll = document.getElementsByClassName("collapsible");
  for (var i = 0; i < coll.length; i++) {
    var content = coll[i].nextElementSibling;
    content.style.display = "block";
    coll[i].classList.add("active");
  }
}

var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
    this.classList.toggle("active");
  });
}
</script>

</body>
</html>
"""
        with open(self.html_file_name, 'a') as file:
            file.write(footer)


    def write_to_html_file(self, text, block_type, end_line):
        """
        Writes text with block characters to the HTML file.

        Args:
            text (str): Text to write to HTML file.
            block_type (str): Type of block (start, mid, end).
        """
        ansi_to_html = {
            "30": "black",
            "31": "red",
            "32": "green",
            "33": "yellow",
            "34": "blue",
            "35": "magenta",
            "36": "cyan",
            "37": "white",
            "0": "reset"
        }

        def convert_line_to_html(line, default_color):
            """
            Convert ANSI colored text to HTML.

            Args:
                line (str): Line of text with ANSI color codes.
                default_color (str): Default color to use when no ANSI color code is provided.

            Returns:
                Tuple[str, str]: HTML representation of the colored text and the last used color.
            """
            html_parts = []  # Initialize a list to store HTML parts of the line
            current_color = default_color  # Initialize the current color to default
            parts = re.split(r'(\033\[[\d;]+m)', line)  # Split the line using ANSI escape code as a separator
            for index, part in enumerate(parts):
                if part:
                    if part.startswith("\033["):
                        codes = part[2:-1].split(";")  # Split the escape code to extract components
                        if codes[0] in ansi_to_html:  # Check if the ANSI code has a corresponding HTML color
                            current_color = ansi_to_html[codes[0]]  # Set the current color
                            if current_color == 'reset':
                                html_part = f'</span>'  # Create HTML part with color style
                            else:
                                html_part = f'<span style="color: {current_color}">'  # Create HTML part with color style
                            html_parts.append(html_part)  # Append the HTML part to the list
                    else:
                        #if index > 0 and html_parts and html_parts[-1] == '</span>':
                        if index == 0:
                            html_part = f'<span style="color: {default_color}">{part}'  # Create HTML part with color style
                            html_parts.append(html_part)  # Append the HTML part to the list
                        else:
                            html_part = f'{part}'  # Create HTML part with color style
                            html_parts.append(html_part)  # Append the HTML part to the list
            html_parts.append(f'</span>')
            return "".join(html_parts), current_color  # Join HTML parts to form the final HTML line and return the last used color

        html_text = ""
        if self.use_block:
            default_color = "default"  # Initialize the default color
            html_output_lines = []  # Initialize list to store HTML lines
            last_color = default_color  # Initialize last used color
            
            message_color = "message_dark" if self.message_color_dark else "message_light"

            
            message, last_color = convert_line_to_html(text, last_color)
            if block_type == 'start':
                # start with a </div> to make sure the previous section is closed
                html_text = f"</div><div class=\"{message_color}\">\n  <h1 class=\"collapsible\">{message}</h1>\n  <div class=\"content\">"
                self.message_color_dark = not self.message_color_dark
            elif block_type == 'mid':
                if end_line:
                    html_text = f"    <p>{message}</p>"
                else:
                    html_text = f"    <p>{message}"
                    self.second_part = True
            elif block_type == 'none_second_part':
                if self.add_div:
                    html_text = f"{message}</p>\n  </div>"
                    self.add_div = False
                else:
                    html_text = f"{message}</p>"
            elif block_type == 'end':
                if end_line:
                    html_text = f"    <p>{message}</p>\n  </div>"
                else:
                    html_text = f"    <p>{message}"
                    self.add_div = True

        with open(self.html_file_name, 'a') as file:
            file.write(html_text + "\n") if end_line else file.write(html_text)

