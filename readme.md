#pyDStools - python module for interacting with Directory Service framework on OS X

pyDStools is a python module for directly querying information in Directory Service (which includes local accounts as well as directory services a Mac may be bound to - like Active Directory, Open Directory, etc.). It uses the ctypes python module to directly wrap the C functions used for accessing Directory Services, instead of wrapping the output of dscl / bash commands.

##Credits

- pyDStools is written by pudquick@github 

##License

pyDStools is released under a standard MIT license.

  Permission is hereby granted, free of charge, to any person
	obtaining a copy of this software and associated documentation files
	(the "Software"), to deal in the Software without restriction,
	including without limitation the rights to use, copy, modify, merge,
	publish, distribute, sublicense, and/or sell copies of the Software,
	and to permit persons to whom the Software is furnished to do so,
	subject to the following conditions:

	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
	BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
	ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
