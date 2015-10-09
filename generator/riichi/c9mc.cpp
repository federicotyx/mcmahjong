#include <iostream>
#include <fstream>
#include "ps.hpp"
#include "rchmcevent.hpp"

using namespace std;

int main()
{
	int times = 100000000;
	ps aps;
	std::ofstream os("c9o.rmj", ios::out | ios::binary);
	for (int ti = 0; ti < times; ++ti)
	{
		aps.reset();
		rchmcevent re;
		re.init(aps);
		//now choose one
		int s1 = 0;
		int s2 = 0;
		int s3 = 0;
		bool p1 = true;
		bool p2 = true;
		bool p3 = true;
		for (int i = 0; i < 9; ++i)
		{
			s1 += re.sp()[i];
			s2 += re.sp()[i + 9];
			s3 += re.sp()[i + 18];
		}
		if (re.sp()[0] > 3)
		{
			p1 = false;
		}
		if (re.sp()[9] > 3)
		{
			p2 = false;
		}
		if (re.sp()[18] > 3)
		{
			p3 = false;
		}
		if (re.sp()[8] > 3)
		{
			p1 = false;
		}
		if (re.sp()[17] > 3)
		{
			p2 = false;
		}
		if (re.sp()[26] > 3)
		{
			p3 = false;
		}
		for (int i = 1; i < 8; ++i)
		{
			if (re.sp()[i] > 1)
			{
				p1 = false;
			}
			if (re.sp()[i + 9] > 1)
			{
				p1 = false;
			}
			if (re.sp()[i + 18] > 1)
			{
				p1 = false;
			}
		}
		if (!p1)
		{
			s1 = 0;
		}
		if (!p2)
		{
			s2 = 0;
		}
		if (!p3)
		{
			s3 = 0;
		}
		int hs = 0;
		uint8_t s;//0:running, 1: failed, 2: finished
		if (s1 > s2)
		{
			if (s1 > s3)
			{
				s = 0;
				hs = 0;
			}
			else if (s1 == s3)
			{
				s = 1;
			}
			else
			{
				s = 0;
				hs = 2;
			}
		}
		else if (s1 == s2)
		{
			s = 1;
		}
		else
		{
			if (s2 < s3)
			{
				s = 0;
				hs = 2;
			}
			else if (s2 == s3)
			{
				s = 1;
			}
			else
			{
				s = 0;
				hs = 1;
			}
		}
		if (s == 1)
		{
			//re.set_status(s);
			//re.write_simple(os);
			continue;
		}
		if (re.sp()[9 * hs] == 3 && re.sp()[9 * hs + 8] == 3)
		{
			bool flag = true;
			for (int i = 1; i < 8; ++i)
			{
				if (re.sp()[i + 9 * hs] != 1)
				{
					flag = false;
					break;
				}
			}
			if (flag)
			{
				s = 2;
			}
		}
		int xm = 0;
		while (s == 0)
		{
			++xm;
			if (xm > 20)
			{
				break;
			}
			re.draw(aps);
			for (int i = 0; i < 34; ++i)
			{
				if (re.sp()[i] != 0 && (i / 9) != hs)
				{
					re.remove(i);
					break;
				}
			}
			if (re.sp()[9 * hs] > 3)
			{
				s = 1;
			}
			else if (re.sp()[9 * hs + 8] > 3)
			{
				s = 1;
			}
			else
			{
				for (int i = 1; i < 8; ++i)
				{
					if (re.sp()[9 * hs + i] > 1)
					{
						s = 1;
						break;
					}
				}
			}
			if (s == 0)
			{
				if (re.sp()[9 * hs] == 3 && re.sp()[9 * hs + 8] == 3)
				{
					bool flag = true;
					for (int i = 1; i < 8; ++i)
					{
						if (re.sp()[i + 9 * hs] != 1)
						{
							flag = false;
							break;
						}
					}
					if (flag)
					{
						s = 2;
					}
				}
			}
		}
		if (s == 2)
		{
			re.set_status(s);
			re.write_human(os);
		}
		if (ti % 100000 == 0)
		{
			cerr << "Finished " << ti << "\r";
		}
	}
	return 0;
}
