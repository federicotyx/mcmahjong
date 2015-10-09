#include "rchmcevent.hpp"
#include "rawio.hpp"
#include "cvs.hpp"

rchmcevent::rchmcevent()
{
	for (int i = 0; i < 34; ++i)
	{
		_sp[i] = 0;
	}
}

void rchmcevent::init(ps& aps)
{
	for (int i = 0; i < 13; ++i)
	{
		++_sp[aps.next()];
	}
	for (int i = 0; i < 34; ++i)
	{
		_isp[i] = _sp[i];
	}
}

void rchmcevent::draw(ps& aps)
{
	int8_t t = aps.next();
	++_sp[t];
	_vps.push_back(t);
}

void rchmcevent::remove(int8_t a)
{
	--_sp[a];
	_vps.push_back(a);
}


void rchmcevent::write_binary(std::ostream& os)
{
	int8_t tsp[13];
	conv34to13(_isp, tsp);
	for (int i = 0; i < 13; ++i)
	{
		wat::write_raw(os, tsp[i]);
	}
	wat::write_raw<uint8_t>(os, _vps.size());
	for (int i = 0; i < _vps.size(); ++i)
	{
		wat::write_raw(os, _vps[i]);
	}
	wat::write_raw(os, _status);
}

void rchmcevent::read_binary(std::istream& is)
{
	int8_t tsp[13];
	for (int i = 0; i < 13; ++i)
	{
		wat::read_raw(is, tsp[i]);
	}
	conv13to34(tsp, _sp);
	for (int i = 0; i < 34; ++i)
	{
		_isp[i] = _sp[i];
	}
	int s = wat::read_raw<uint8_t>(is);
	_vps.resize(s);
	for (int i = 0; i < s; ++i)
	{
		wat::read_raw(is, _vps[i]);
	}
	wat::read_raw(is, _status);
}

void rchmcevent::write_simple(std::ostream& os)
{
	int8_t tsp[13];
	conv34to13(_isp, tsp);
	for (int i = 0; i < 13; ++i)
	{
		os << b2t(tsp[i]);
	}
	os << " ";
	os << _vps.size() / 2;
	os << " ";
	for (int i = 0; i < _vps.size() / 2; ++i)
	{
		os << b2t(_vps[2 * i]);
		os << b2t(_vps[2 * i + 1]);
		os << " ";
	}
	os << " ";
	os << int(_status);
	os << std::endl;
}

void rchmcevent::write_human(std::ostream& os)
{
	int8_t tsp[13];
	int8_t t[34];
	for (int i = 0; i < 34; ++i)
	{
		t[i] = _isp[i];
	}
	os << "<event>" << std::endl;
	for (int i = 0; i < _vps.size() / 2; ++i)
	{
		conv34to13(t, tsp);
		for (int j = 0; j < 13; ++j)
		{
			os << b2t(tsp[j]);
		}
		os << " ";
		os << b2t(_vps[2 * i]);
		os << " ";
		os << b2t(_vps[2 * i + 1]);
		os << std::endl;
		++t[_vps[2 * i]];
		--t[_vps[2 * i + 1]];
	}
	conv34to13(t, tsp);
	for (int j = 0; j < 13; ++j)
	{
		os << b2t(tsp[j]);
	}
	os << " " << int(_status);
	os << std::endl;
	os << "</event>" << std::endl;
}

void rchmcevent::conv34to13(int8_t a[34], int8_t b[13])
{
	int k = 0;
	for (int i = 0; i < 34; ++i)
	{
		for (int j = 0; j < a[i]; ++j)
		{
			b[k] = i;
			++k;
		}
	}
}

void rchmcevent::conv13to34(int8_t a[13], int8_t b[34])
{
	for (int i = 0; i < 13; ++i)
	{
		++b[a[i]];
	}
}
