#ifndef _WAT_RAWIO_HPP
#define _WAT_RAWIO_HPP 11

#include <iostream>
#include <type_traits>
#include <string>
#include <complex>

namespace wat
{
	//for read_raw, there are two version

	//pod template version
	//enable if pod
	template<typename T, typename = typename std::enable_if<std::is_pod<T>::value>::type>
	void read_raw(std::istream& is, T& value)
	{
		is.read(reinterpret_cast<char*>(&value), sizeof(value));
	}

	//the overloads for two arguments version should be put before
	//the one argument template version

	//for std::string
	void read_raw(std::istream& is, std::string& s);

	//for std::complex<T>
	template<typename T>
	void read_raw(std::istream& is, std::complex<T>& value)
	{
		T tmp;
		read_raw(is, tmp);
		value.real(tmp);
		read_raw(is, tmp);
		value.imag(tmp);
	}

	//for no pod datatype, this only works if the corresponding two arg version read_raw put before this
	//function
	template<typename T>
	T read_raw(std::istream& is)
	{
		T value;
		read_raw(is, value);
		return value;
	}

	//enable if pod
	template<typename T, typename = typename std::enable_if<std::is_pod<T>::value>::type>
	void write_raw(std::ostream& os, const T& value)
	{
		os.write(reinterpret_cast<const char*>(&value), sizeof(value));
	}


	//for std::string
	void write_raw(std::ostream&, const std::string& s);

	//for std::complex<T>
	template<typename T>
	void write_raw(std::ostream& os, const std::complex<T>& value)
	{
		write_raw(os, value.real());
		write_raw(os, value.imag());
	}

}

#endif // _WAT_RAWIO_HPP
