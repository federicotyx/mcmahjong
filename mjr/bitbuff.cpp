#include "bitbuff.hpp"

void bitbuff::read(uint8_t& r)
{
	r = 0;
	if (_bit == 0)
	{
		r |= _data[_pos];
	}
	else
	{
		r |= _data[_pos] << _bit;
		r |= _data[_pos + 1] >> (8 - _bit);
	}
}

void bitbuff::read(uint16_t& r)
{
	r = 0;
	if (_bit == 0)
	{
		r |= _data[_pos] << 8;
		r |= _data[_pos + 1];
	}
	else
	{
		r |= _data[_pos] << (8 + _bit);
		r |= _data[_pos + 1] << (_bit);
		r |= _data[_pos + 2] >> (8 - _bit);
	}
}

void bitbuff::write(uint8_t d)
{
	if (_bit == 0)
	{
		_data[_pos] = d;
	}
	else
	{
		_data[_pos] &= 0xff << (8 - _bit);
		_data[_pos] |= d >> _bit;
		_data[_pos + 1] = d;
	}
}
void bitbuff::write(uint16_t d)
{
	if (_bit == 0)
	{
		_data[_pos] = d >> 8;
		_data[_pos + 1] = d & 0xff;
	}
	else
	{
		_data[_pos] &= 0xff << (8 - _bit);
		_data[_pos] |= d >> (8 + _bit);
		_data[_pos + 1] = (d >> _bit) & 0xff;
		_data[_pos + 2] = (d << (8 - _bit)) & 0xff;
	}
}

void bitbuff::write_and_add(const std::string& str)
{
	for (uint32_t i = 0; i < str.size(); ++i)
	{
		write(uint8_t(str[i]));
		add(8);
	}
}
