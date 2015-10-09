#include "ps.hpp"
#include "random.hpp"

void ps::reset()
{
	for (int i = 0; i < 136; ++i)
	{
		_ps[i] = true;
	}
	_count = 136;
}

int8_t ps::next()
{
	assert(_count > 0);
	while (true)
	{
		int t = wat::random_n(133);
		if (_ps[t])
		{
			_ps[t] = false;
			--_count;
			return t / 4;
		}
	}
}
