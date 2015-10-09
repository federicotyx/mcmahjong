#ifndef MCMJ_RCHMC_RCHMCEVENT_HPP
#define MCMJ_RCHMC_RCHMCEVENT_HPP 11

#include <vector>
#include <cstdint>
#include <iostream>

#include "ps.hpp"

class rchmcevent
{
	public:
	rchmcevent();
	void init(ps& aps);
	void draw(ps& aps);
	void remove(int8_t a);
	int8_t* sp() { return _sp; }
	const int8_t* sp() const { return _sp; }

	void set_status(uint8_t s) { _status = s; }

	void write_binary(std::ostream& os);
	void read_binary(std::istream& is);

	void write_simple(std::ostream& os);

	void write_human(std::ostream& os);
	protected:
	void conv34to13(int8_t a[34], int8_t b[13]);
	void conv13to34(int8_t a[13], int8_t b[34]);
	int8_t _status;
	int8_t _sp[34];
	int8_t _isp[34];
	std::vector<int8_t> _vps;
};

#endif
