"""
Update jdhao/nvim-config for personal customization without breaking git syncing.
"""
import os
import pathlib
from argparse import ArgumentParser

HOME=pathlib.Path(os.environ["HOME"])

def count_brackets(line):
    """
    Count the number of brackets in a line to assist with finding
    the line where a bracket closes.
    """
    brackets = 0
    for _s in line:
        if _s == "{":
            brackets -= 1
        elif _s == "}":
            brackets += 1
    return brackets


def add_copilot_plugin():
    """
    Add the copilot plugin
    """
    with open(HOME / ".config/nvim/lua/plugin_specs.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    start_line = None
    end_line = None
    for i, line in enumerate(lines):
        # print(line.rstrip())
        if "local plugin_specs" in line:
            start_line = i
            suffix = line.split("local plugin_specs")[1]
            bracket_diff = count_brackets(suffix)
            depth = bracket_diff
        elif start_line is not None and end_line is None:
            bracket_diff = count_brackets(line)
            if bracket_diff != 0:
                depth += bracket_diff
            if depth == 0:
                end_line = i
                print(start_line, end_line)
    print(lines[start_line])
    print(lines[end_line])

    copilot_insert = """  {
    "zbirenbaum/copilot.lua",
    cmd = "Copilot",
    event = "InsertEnter",
    config = function()
      require("copilot").setup({
        suggestion = {
          auto_trigger=true,
        }
      })
    end,
  },
"""
    print(f"Inserted in lua/plugin_specs.lua: {end_line}")
    lines.insert(end_line, copilot_insert)
    for _l in lines[end_line-10:end_line+2]:
        print(_l.rstrip())

    with open(HOME / ".config/nvim/lua/plugin_specs.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)


def update_keymappings():
    """
    Add better keybindings for copilot

    # Old notes
    # +-- Copilot config
    # +-- Consider also: https://github.com/zbirenbaum/copilot-cmp
    # +-- keymap.set("i", "<C-J>", 'copilot#Accept("<CR>")', { silent = true, expr = true })

    """
    with open(HOME / ".config/nvim/lua/mappings.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    # Remove remap for H & L, disables beginning/end of line shortcut
    to_comment = [
        'keymap.set({ "n", "x" }, "H", "^")',
        'keymap.set({ "n", "x" }, "L", "g_")',
    ]
    for i_line,line in enumerate(lines):
        if any(x in line for x in to_comment):
            lines[i_line] = "-- " + line

    lines.append('keymap.set("n", "F", "za")\n')
    lines.append(' -- see https://vi.stackexchange.com/q/12607/15292\n')
    lines.append('keymap.set("x", "$", "g_")')


    with open(HOME / ".config/nvim/lua/mappings.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)
    print("Updated mappings.lua")


def update_globals():
    with open(HOME / ".config/nvim/lua/globals.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    appender = [
        '',
        'vim.o.foldmethod = "expr"',
        'vim.o.foldexpr = "nvim_treesitter#foldexpr()"',
        'vim.o.foldlevel = 99',
        'vim.o.foldenable = false',
        '',
        """vim.g.copilot_no_tab_map = true
vim.g.copilot_assume_mapped = true
vim.g.copilot_filetypes = {
  ["*"] = false,
  ["scala"] = true,
  ["javascript"] = true,
  ["typescript"] = true,
  ["lua"] = false,
  ["rust"] = true,
  ["c"] = true,
  ["c#"] = true,
  ["c++"] = true,
  ["go"] = true,
  ["python"] = true,
}""",
    ]
    for _l in appender:
        lines.append(_l + "\n")

    with open(HOME / ".config/nvim/lua/globals.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)

    print("Updated globals.lua")


def update_linter_symbols():
    """
    Update the linter signals to be more readable

    +-- some good arrows:
    +--  ➡ ➜ ➤ ➩ ➪ ➫ ➬ ➭ ➮ ➯ ➱ ➲ ➳ ➵ ➸ ➻ ➺ ➼ ➽
    +--       
    +-- some good info / idea:
    +-- � ⓘ   ℹ         
    +-- some other fun icons
    +--                       
    """
    with open(HOME / ".config/nvim/lua/config/lsp.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("fn.sign_define"):
            if "DiagnosticSignError" in line:
                lines[i] = 'fn.sign_define("DiagnosticSignError", { text = "", texthl = "DiagnosticSignError" })\n'
                print("Updated DiagnosticSignError")
            if "DiagnosticSignWarn" in line:
                lines[i] = 'fn.sign_define("DiagnosticSignWarn", { text = "", texthl = "DiagnosticSignWarn" })\n'
                print("Updated DiagnosticSignWarn")
            if "DiagnosticSignInfo" in line:
                lines[i] = 'fn.sign_define("DiagnosticSignInfo", { text = "", texthl = "DiagnosticSignInfo" })\n'
                print("Updated DiagnosticSignInfo")
            if "DiagnosticSignHint" in line:
                lines[i] = 'fn.sign_define("DiagnosticSignHint", { text = "ℹ", texthl = "DiagnosticSignHint" })\n'
                print("Updated DiagnosticSignHint")

    with open(HOME / ".config/nvim/lua/config/lsp.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)

    print("Updated linter_signals.lua")

def update_colorscheme(color):
    color = color or "onedark"
    with open(HOME / ".config/nvim/lua/colorschemes.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    lines.append(f"\nvim.cmd('colorscheme {color}')")

    with open(HOME / ".config/nvim/lua/colorschemes.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)

    print("Updated colorscheme.lua")

def update_gitsigns():
    with open(HOME / ".config/nvim/lua/config/gitsigns.lua", encoding='utf-8') as _f:
        lines = _f.readlines()

    check_section=False
    start_brackets=False
    start_line=None
    end_line=None
    for i, line in enumerate(lines):
        if line.startswith("gs.setup"):
            print(f"Found gitsigns setup {i}")
            check_section=True
            bracket_depth = None
            continue
        if check_section:
            if line.replace(" ","").startswith("signs="):
                print("Found signs")
                check_section=False
                start_brackets = True
                start_line = i

        if start_brackets:
            delta = count_brackets(line)
            if bracket_depth is None and delta != 0:
                bracket_depth = 0
            if bracket_depth is not None:
                bracket_depth += delta
            if bracket_depth == 0:
                end_line = i
                start_brackets = False

    if start_line is not None and end_line is not None:
        print(f"Found gitsigns section: {start_line} - {end_line}")
        lines = lines[:start_line] + ["""  signs = {
    add = { hl = "GitSignsAdd", text = "⁺", numhl = "GitSignsAddNr", linehl = "GitSignsAddLn" },
    change = { hl = "GitSignsChange", text = "˜", numhl = "GitSignsChangeNr", linehl = "GitSignsChangeLn" },
    delete = { hl = "GitSignsDelete", text = "_", numhl = "GitSignsDeleteNr", linehl = "GitSignsDeleteLn" },
    topdelete = { hl = "GitSignsDelete", text = "‾", numhl = "GitSignsDeleteNr", linehl = "GitSignsDeleteLn" },
    changedelete = { hl = "GitSignsChange", text = "│", numhl = "GitSignsChangeNr", linehl = "GitSignsChangeLn" },
  },
"""] + lines[end_line+1:]
        print("".join(lines[start_line-3:start_line+2]))

    word_diff_line = None
    for i, line in enumerate(lines):
        if line.replace(" ", "").startswith("word_diff="):
            word_diff_line = i
            print (f"Found word_diff: {line}")
            break
    if word_diff_line is not None:
        lines[word_diff_line] = "  word_diff = false,\n"

    with open(HOME / ".config/nvim/lua/config/gitsigns.lua", "w", encoding='utf-8') as _f:
        _f.writelines(lines)


if __name__=="__main__":
    parser = ArgumentParser(description="Update nvim-config")
    parser.add_argument("--copilot", action="store_true", help="Add copilot plugin")
    parser.add_argument("--keymappings", action="store_true", help="Update keymappings")
    parser.add_argument("--globals", action="store_true", help="Update globals")
    parser.add_argument("--linter_symbols", action="store_true", help="Update linter symbols")
    parser.add_argument("--colorscheme", type=str, default=None, help="Update colorscheme to selected")
    parser.add_argument("--gitsigns", action="store_true", help="Update gitsigns")
    parser.add_argument("--all", action="store_true", help="Update all")
    args = parser.parse_args()

    if args.copilot or args.all:
        add_copilot_plugin()
    if args.keymappings or args.all:
        update_keymappings()
    if args.globals or args.all:
        update_globals()
    if args.linter_symbols or args.all:
        update_linter_symbols()
    if args.colorscheme or args.all:
        update_colorscheme(args.colorscheme)
    if args.gitsigns or args.all:
        update_gitsigns()
