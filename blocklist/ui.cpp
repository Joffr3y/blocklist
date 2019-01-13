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

#include <Python.h>

#include <iostream>
#include <iomanip>      // setw
#include <cmath>        // pow
#include <string>

#include "ui.hpp"


static PyObject* UIError;   // UI Python Exception


/* Class Color
-----------------------------------------------------------------------------*/

std::string
Color::getvalue(const std::string& colorkey) const {
    std::string color;

    try {
        color = colormap.at(colorkey);
    } catch (std::out_of_range& exc) {
        std::string msg = '"' + colorkey + '"' + " colorkey is unknown";
        PyErr_SetString(UIError, msg.c_str());
    }
    return color;
}

std::string
Color::color(const std::string& str, const std::string& colorkey) const {
    return  "\033[3" + getvalue(colorkey) + str + "\033[0;0m";
}

template<class T>
std::string
Color::bold(const T& str) const {
    return std::string("\033[1m") + str + "\033[0;0m";
}

template<class T>
std::string
Color::bold(const T& str, const std::string& colorkey) const {
    return "\033[1;3" + getvalue(colorkey) + str + "\033[0;0m";
}

std::string
Color::background(const std::string& str, const std::string& colorkey) const {
    return "\033[4" + getvalue(colorkey) + str + "\033[0;0m";
}


/* Class UI
-----------------------------------------------------------------------------*/

template<class T>
std::string
UI::repeat(const int& num, const T& ch) const {
    std::string str;

    for (int i = 0; i < num; ++i)
        str += ch;

    return str;
}

unsigned int
UI::termwidth() const {
    struct winsize terminal;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &terminal);

    return terminal.ws_col;
}

void
UI::info(
        const std::string& msg, const std::string& color,
        const std::string& prefix) const {
    std::cout << bold(prefix, color) << ' ' << bold(msg) << std::endl;
}

void
UI::err(const std::string& msg, const std::string& color) const {
    std::cerr << bold(msg, color) << std::endl;
}

std::string
UI::progressbar(const unsigned int& step, const unsigned int& width) const {
    using std::string;

    string sep = bold('|');
    string bar = bold(repeat(step, "▓"), "blue") + repeat((width - step), "░");

    return sep + bar + sep;
}

std::string
UI::index(const unsigned int& index, const unsigned int& total) const {
    std::string t = std::to_string(total);
    std::string i = std::to_string(index);

    int lent = t.size();
    int leni = i.size();

    if (leni == lent)
        return i + '/' + t;

    return repeat((lent - leni), ' ') + i + '/' + t;
}

std::string
UI::loading(const unsigned int& value, const unsigned int& total) const {
    using std::to_string;

    const int kio = pow(2, 10);
    const int mio = pow(2, 20);

    if (total < kio)
        return ' ' + to_string(value)       + '/' + to_string(total)       + " o   ";
    else if (total < mio)
        return ' ' + to_string(value / kio) + '/' + to_string(total / kio) + " Kio ";
    else
        return ' ' + to_string(value / mio) + '/' + to_string(total / mio) + " Mio ";
}

void
UI::statusprocess(
        const std::string& info, const double& value,
        const double& total, const bool& loading) const {
    float coef = 1;

    if (value && total)
        coef = value / total;

    const unsigned int percent   = coef * 100;
    const unsigned int termwidth = this->termwidth();
    const unsigned int barwidth  = termwidth / 2;
    const unsigned int step      = coef * barwidth;

    std::string loaded;
    if (loading)
        loaded = this->loading(value, total);

    // | bar |  +2 chars
    // percent  +4 chars

    unsigned int minwidth = info.size() + loaded.size() + barwidth + 6;
    std::string bar;

    if (termwidth <= minwidth)
        minwidth -= barwidth + 2;
    else
        bar = progressbar(step, barwidth);

    std::cout << '\r'
        << info
        << repeat(termwidth - minwidth - 1, ' ')
        << loaded
        << bar
        << std::setw(4)
        << percent << '%';
    std::cout.flush();
}


/* Python module
-----------------------------------------------------------------------------*/

UI uiobj;   // UI instance


PyDoc_STRVAR(ui_doc,
R"(User Interface

Provides the necessary functions to color the output of scripts,
and add a progressbar for status process.

Str colors availables:
'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.)"
);

/* ui.color */

PyDoc_STRVAR(color_doc,
R"(color(str, color)
--

Return str with color format)"
);

static PyObject*
color(PyObject* self, PyObject* args) {
    const char *str, *color;

    if (!PyArg_ParseTuple(args, "ss", &str, &color))
        return NULL;

    return PyUnicode_FromString(uiobj.color(str, color).c_str());
}

/* ui.bold */

PyDoc_STRVAR(bold_doc,
R"(bold(str, color=None)
--

Return str with bold format)"
);

static PyObject*
bold(PyObject* self, PyObject *args) {
    const char* str;
    const char* color = NULL;

    if (!PyArg_ParseTuple(args, "s|s", &str, &color))
        return NULL;
    else if (color == NULL)
        return PyUnicode_FromString(uiobj.bold(str).c_str());

    return PyUnicode_FromString(uiobj.bold(str, color).c_str());
}

/* ui.background */

PyDoc_STRVAR(background_doc,
R"(background(str, color)
--

Return str with background format)"
);

static PyObject*
background(PyObject* self, PyObject *args) {
    const char *str, *color;

    if (!PyArg_ParseTuple(args, "ss", &str, &color))
        return NULL;

    return PyUnicode_FromString(uiobj.background(str, color).c_str());
}

/* ui.statusprocess */

PyDoc_STRVAR(statusprocess_doc,
R"(statusprocess(info, value, total, loading=True)
--

Print status process with a progressbar

Parameters :

    info    : str informations
    value   : int or float curent value
    total   : int or float total value
    loading : bool (optional), print octet loading

Example :

>>> ui.statusprocess('File loading', 54546555464, 42573243455); print()
File loading     2867/3737 Mio |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░|  76%)"
);

static PyObject*
statusprocess(PyObject* self, PyObject* args) {
    const char* info;
    unsigned int value, total;
    int loading = 1;    /* bool loading = true; */

    if (!PyArg_ParseTuple(args, "sII|p", &info, &value, &total, &loading))
        return NULL;

    uiobj.statusprocess(info, value, total, loading);
    Py_RETURN_NONE;
}

/* ui.index */

PyDoc_STRVAR(index_doc,
R"(index(value, total)
--

Return str index progression

Example :

>>> for i in range(0, 101, 25): print('(' +  ui.index(i, 100) + ')')
...
(  0/100)
( 25/100)
( 50/100)
( 75/100)
(100/100))"
);

static PyObject*
index(PyObject* self, PyObject* args) {
    unsigned int value, total;

    if (!PyArg_ParseTuple(args, "II", &value, &total))
        return NULL;

    return PyUnicode_FromString(uiobj.index(value, total).c_str());
}

/* ui.progressbar */

PyDoc_STRVAR(progressbar_doc,
R"(progressbar(step, width)
--

Return str progressbar

Parameters :

    width : int chars width number
    step  : (value / total) * width)"
);

static PyObject*
progressbar(PyObject* self, PyObject* args) {
    unsigned int step, width;

    if (!PyArg_ParseTuple(args, "II", &step, &width))
        return NULL;

    return PyUnicode_FromString(uiobj.progressbar(step, width).c_str());
}

/* ui.info */

PyDoc_STRVAR(info_doc,
R"(info(msg, color='blue', prefix='::')
--

Print a highlighted message with a prefix in stdout)"
);

static PyObject*
info(PyObject* self, PyObject* args) {
    const char* msg;
    const char* color  = "blue";
    const char* prefix = "::";

    if (!PyArg_ParseTuple(args, "s|sss", &msg, &color, &prefix))
        return NULL;

    uiobj.info(msg, color, prefix);
    Py_RETURN_NONE;
}

/* ui.err */

PyDoc_STRVAR(err_doc,
R"(err(msg, color=None)
--

Print a highlighted message in stderr)"
);

static PyObject*
err(PyObject* self, PyObject* args) {
    const char* msg;
    const char* color = "";

    if (!PyArg_ParseTuple(args, "s|s", &msg, &color))
        return NULL;

    uiobj.err(msg, color);
    Py_RETURN_NONE;
}

/* Methods definition */

static PyMethodDef UIMethods[] = {
    { "color"          , color          , METH_VARARGS  , color_doc          },
    { "bold"           , bold           , METH_VARARGS  , bold_doc           },
    { "background"     , background     , METH_VARARGS  , background_doc     },
    { "statusprocess"  , statusprocess  , METH_VARARGS  , statusprocess_doc  },
    { "index"          , index          , METH_VARARGS  , index_doc          },
    { "progressbar"    , progressbar    , METH_VARARGS  , progressbar_doc    },
    { "info"           , info           , METH_VARARGS  , info_doc           },
    { "err"            , err            , METH_VARARGS  , err_doc            },
    { NULL             , NULL           , 0             , NULL               }
};

static struct PyModuleDef ui = {
    PyModuleDef_HEAD_INIT,
    "ui",
    ui_doc,
    -1,
    UIMethods
};

/* Module initialization */

PyMODINIT_FUNC
PyInit_ui(void) {
    PyObject* m = PyModule_Create(&ui);

    if (m == NULL)
        return NULL;

  // Add ui.error Exception

    UIError = PyErr_NewException("ui.error", NULL, NULL);
    Py_INCREF(UIError);
    PyModule_AddObject(m, "error", UIError);

  // --

    return m;
}
