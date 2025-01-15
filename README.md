# Nestris

A recreation of [Tetris (NES)](https://en.wikipedia.org/wiki/Tetris_(NES_video_game)) using modern NES development tools.

Traditionally, NES games were written in raw 6502 assembly, and it still remains the most dominant strategy for modern homebrew games. This approach offers the finest degree of control over the hardware, but is much less ergonomic than higher-level languages. However, in the many years since the last official NES was made, newer tools have been made to address these shortcomings. In essence, this project imagines how the codebase of NES Tetris would look like if these modern tools were used. This codebase build a `.nes` file, which can be run via software through an emulator or on hardware with a flash cart.

I have the following goals:
- Have an easily modifiable codebase for faster romhack creation.
- Benchmark NESFab's performance against the original assembly.
- Gain experience with tools I haven't used before.

Replicating the gameplay and visual/audio elements of an existing game has inherent copyright risks. This project is primarily intended as a personal exploration and learning exercise.

## Implementation strategy

I use the NES Tetris [disassembly](https://github.com/CelestialAmber/TetrisNESDisasm) as the blueprint for all expected behavior. In addition, I also cross-reference the logic with [meta_nestris](https://github.com/negative-seven/meta_nestris), which specifies the core game logic. While I intend to preserve as much of the original behavior as possible, this does not include glitches like the game crash, which are dependent on the timing of CPU cycles. However, it may be possible to implement a simulation similar to the [crash detection](https://github.com/kirjavascript/TetrisGYM/pull/61) used in TetrisGYM.

## Tools

### NESFab

[NESFab](https://pubby.games/nesfab.html) is a programming language specifically targeted for NES games. It abstracts many low-level tasks associated with 6502 programming, like memory allocation and bank-switching, while maintaining [reasonable performance](https://pubby.games/codegen.html) when compared to other modern approaches.

I've experimented with it on a couple of projects (like [rollTool](https://github.com/fractal161/rollTool)) and have enjoyed it immensely, finding it strikes a nice balance between high-level logic and the low-level control I expect when working with the NES, so I wanted to try it out on a larger project.

### NEXXT

[NEXXT Studio](https://frankengraphics.itch.io/nexxt) is a graphics editor for NES games. Its main feature is enforcing the graphical restrictions of the NES, which include [palette](https://www.nesdev.org/wiki/PPU_palettes) and [tile](https://www.nesdev.org/wiki/PPU_pattern_tables) restrictions, so anything you can design here can necessarily be replicated on original hardware.

Prior to this, I had been using GIMP to edit the [pattern tables](https://www.nesdev.org/wiki/PPU_pattern_tables) and GHex to edit [nametables](https://www.nesdev.org/wiki/PPU_nametables), which had many inconveniences, so I was particularly eager to make the leap to something more tailor-made to the NES game use-case.

### Famitracker

[Famitracker](http://famitracker.com/) is a popular music editor for composing NES/Famicom music. Like NEXXT, it's designed with the limitations of the target hardware in mind, and allows you to control the raw audio channels directly while still offering higher-level primitives than the direct [APU registers](https://www.nesdev.org/wiki/APU#Registers).

This project rewrites the music and sound effects using Famitracker, which are then integrated through NESFab's PUF music engine. The NES Tetris audio engine is probably the most confusing part of the code, feeling especially hacky and scattered, so it's an ideal candidate to be replaced.

## Setup

This project uses [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), so you'll want to clone this repository using `git clone --recurse-submodules`, or use `git submodule update --init --recursive` if you've already cloned it. From there, enter the `nesfab` directory and follow its [build instructions](https://github.com/pubby/nesfab?tab=readme-ov-file#building). To work with graphics or audio, you'll want to install [NEXXT](https://frankengraphics.itch.io/nexxt) or [Famitracker](http://famitracker.com/) respectively, though this isn't required to build the project.

From here, `nestris` can be built by running `make`.

## Benchmarks

Coming soon!
