#!/bin/bash

# extracts the skin from the program config file

get_skin () {
    local macro_string=$(grep '^macro("gfx_data", "\(.*\)")$' config.fab)
    local skin=${macro_string#'macro("gfx_data", "'}
    skin=${skin%'")'}
    echo $skin
}
get_skin
unset -f get_skin
