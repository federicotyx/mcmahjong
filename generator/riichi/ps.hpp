#ifndef MCMJ_RCHMC_PS_HPP
#define MCMJ_RCHMC_PS_HPP 11

#include <cstdint>

class ps
{
	public:
	void reset();
	int8_t next();
	protected:
	int _count;
	bool _ps[136];
};

#endif
