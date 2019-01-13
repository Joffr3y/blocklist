/* Copyright (C) 2018 Joffrey Darcq
 *
 * This file is part of Blocklist.
 *
 * Blocklist is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Blocklist is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public licenses
 * along with Blocklist.  If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef _BLOCKLIST_UI_HPP_
#define _BLOCKLIST_UI_HPP_

#include <sys/ioctl.h>
#include <unistd.h>

#include <map>
#include <string>


class Color {
 private:
    std::map<std::string, std::string> colormap = {
        { "black"   , "0m" },
        { "red"     , "1m" },
        { "green"   , "2m" },
        { "yellow"  , "3m" },
        { "blue"    , "4m" },
        { "magenta" , "5m" },
        { "cyan"    , "6m" },
        { "white"   , "7m" }
    };

    std::string getvalue(
        const std::string& colorkey
    ) const;

 public:
    std::string color(
        const std::string& str,
        const std::string& colorkey
    ) const;

    template<class T>
    std::string bold(
        const T& str
    ) const;

    template<class T>
    std::string bold(
        const T& str,
        const std::string& colorkey
    ) const;

    std::string background(
        const std::string& str,
        const std::string& colorkey
    ) const;
};

class UI: public Color {
 private:
    template<class T>
    std::string repeat(
        const int& num, const T& ch
    ) const;

 public:
    unsigned int termwidth(
    ) const;

    void info(
        const std::string & msg,
        const std::string & color  = "blue",
        const std::string & prefix = "::"
    ) const;

    void err(
        const std::string& msg,
        const std::string& color = "red"
    ) const;

    std::string progressbar(
        const unsigned int& step,
        const unsigned int& width
    ) const;

    std::string index(
        const unsigned int& index,
        const unsigned int& total
    ) const;

    std::string loading(
        const unsigned int& value,
        const unsigned int& total
    ) const;

    void statusprocess(
        const std::string& info,
        const double& value,
        const double& total,
        const bool& loading = true
    ) const;
};

#endif // _BLOCKLIST_UI_HPP_
