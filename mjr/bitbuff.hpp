//bitbuff.hpp
//a bit buff for write bits or read bits

#ifndef MJR_BITBUFF_HPP
#define MJR_BITBUFF_HPP 1

#include <cstdlib>
#include <cstdint>
#include <string>

class bitbuff
{
public:
	bitbuff()
	{
		_data = NULL;
		_pos = 0;
		_bit = 0;
	}
	~bitbuff()
	{
		if (_data != 0)
		{
			delete [] _data;
		}
	}

	void set_data(uint8_t* nd)
	{
		_data = nd;
	}

	uint8_t* get_data()
	{
		return _data;
	}

	uint32_t size()
	{
		if (_bit == 0)
		{
			return _pos;
		}
		else
		{
			return _pos + 1;
		}
	}

	void add(uint32_t n)
	{
		bitadd(n);
	}

	void read(uint8_t& d);
	void read(uint16_t& d);
	void write(uint8_t d);
	void write(uint16_t d);

	void write_and_add(const std::string& str);

private:
	uint8_t* _data;
	uint32_t _pos;
	uint32_t _bit;

	//n must smaller than 16
	inline void bitadd(uint32_t n)
	{
		_bit += n;
		if (_bit >= 8)
		{
			_pos += 1;
			_bit -= 8;
		}
		if (_bit >= 8)
		{
			_pos += 1;
			_bit -= 8;
		}
	}
};


#endif
