#include <iostream>
#include <fstream>
#include <sstream>
#include <libxml++/libxml++.h>
#include <cstdlib>
#include <cassert>
#include "bitbuff.hpp"
#include "tileconv.hpp"

using namespace std;

bitbuff bf;
uint8_t lastdraw;
uint8_t lastdiscard;
bool ingame;

void akaindi(uint8_t a)
{
	if (((a >> 6) & 0x1) == 1)
	{
		bf.write(uint8_t(0x80));//1
	}
	else
	{
		bf.write(uint8_t(0x00));//0
	}
	bf.add(1);
}

void process_node(const xmlpp::Node* node, unsigned int indentation = 0)
{
	const auto node_text = dynamic_cast<const xmlpp::TextNode*>(node);
	const auto node_element = dynamic_cast<const xmlpp::Element*>(node);
	if (node_text)//ignore text node
	{
		return;
	}
	const auto nodename = node->get_name();
	if (nodename == "mjr")
	{
		//init
		uint8_t indi = 0x80;//1xxx xxxx
		bf.write(indi);
		bf.add(1);
	}
	else if (nodename == "info")
	{
		const auto attr = node_element->get_attributes();
		ostringstream oss;
		for (auto it = attr.begin(); it != attr.end(); ++it)
		{
			if (it != attr.begin())
			{
				oss << " ";
			}
			oss << (*it)->get_name() << "=" << (*it)->get_value();
		}
		bf.write_and_add(oss.str());
		bf.write(uint8_t(0));
		bf.add(8);
	}
	else if (nodename == "game")
	{
		ingame = true;
		const auto attr = node_element->get_attributes();
		ostringstream oss;
		for (auto it = attr.begin(); it != attr.end(); ++it)
		{
			if (it != attr.begin())
			{
				oss << " ";
			}
			oss << (*it)->get_name() << "=" << (*it)->get_value();
		}
		bf.write_and_add(oss.str());
		bf.write(uint8_t(0));
		bf.add(8);
	}
	else if (nodename == "score")
	{
		const std::string str = node_element->get_child_text()->get_content();
		istringstream iss(str);
		int16_t s;
		for (int i = 0; i < 4; ++i)
		{
			iss >> s;
			bf.write(uint16_t(s));
			bf.add(16);
		}
	}
	else if (nodename == "init")
	{
		const std::string str = node_element->get_child_text()->get_content();
		vector<uint8_t> v;
		txt2bin(str, v);
		assert(v.size() == 13);
		for (int i = 0; i < v.size(); ++i)
		{
			bf.write(uint8_t(v[i] << 1));
			bf.add(7);
		}
	}
	else if (nodename == "indicator")
	{
		const std::string str = node_element->get_child_text()->get_content();
		uint8_t t = txt2bin(str);
		t <<= 1;
		bf.write(t);
		bf.add(7);
	}
	else if (nodename == "draw")
	{
		uint8_t indi = 0x0;//0xxx xxxx
		bf.write(indi);
		bf.add(1);
		const std::string str = node_element->get_child_text()->get_content();
		uint8_t t = txt2bin(str);
		lastdraw = t;
		t <<= 1;
		bf.write(t);
		bf.add(7);
	}
	else if (nodename == "discard1")
	{
		uint8_t indi = 0x0;//0xxx xxxx
		bf.write(indi);
		bf.add(1);
		const std::string str = node_element->get_child_text()->get_content();
		uint8_t t = txt2bin(str);
		lastdiscard = t;
		t <<= 1;
		bf.write(t);
		bf.add(7);
	}
	else if (nodename == "discard2")
	{
		uint8_t indi = 0x80;//1xxx xxxx
		bf.write(indi);
		bf.add(1);
		lastdiscard = lastdraw;
	}
	else if (nodename == "chi")
	{
		const std::string str = node_element->get_child_text()->get_content();
		vector<uint8_t> v;
		txt2bin(str, v);
		assert(v.size() == 2);
		uint8_t a = std::min(std::min(lastdiscard % 64, v[0] % 64), v[1] % 64);
		uint8_t indi;
		switch ((lastdiscard % 64) - a)
		{
		case 0:
			indi = 0xc8;//1100 1xxx
			break;
		case 1:
			indi = 0xd0;//1101 0xxx
			break;
		case 2:
			indi = 0xd8;//1101 1xxx
			break;
		default:
			break;
		}
		bf.write(indi);
		bf.add(5);
		akaindi(v[0]);
		akaindi(v[1]);
	}
	else if (nodename == "peng")
	{
		const std::string str = node_element->get_child_text()->get_content();
		vector<uint8_t> v;
		txt2bin(str, v);
		assert(v.size() == 2);
		const std::string id = node_element->get_attribute_value("id");
		istringstream iss(id);
		uint8_t iid;
		iss >> iid;
		uint8_t indi = 0xe0;//1110 0xxx
		bf.write(indi);
		bf.add(5);
		bf.write(uint8_t(iid << 6));
		bf.add(2);
		akaindi(v[0]);
		akaindi(v[1]);
	}
	else if (nodename == "angang")
	{
		const std::string str = node_element->get_child_text()->get_content();
		uint8_t t = txt2bin(str);
		t <<= 2;
		uint8_t indi = 0xe8;//1110 10xx
		bf.write(indi);
		bf.add(6);
		bf.write(t);
		bf.add(6);
	}
	else if (nodename == "jiagang")
	{
		const std::string str = node_element->get_child_text()->get_content();
		uint8_t t = txt2bin(str);
		t <<= 1;
		uint8_t indi = 0xec;//1110 110x
		bf.write(indi);
		bf.add(7);
		bf.write(t);
		bf.add(7);
	}
	else if (nodename == "daminggang")
	{
		const std::string id = node_element->get_attribute_value("id");
		istringstream iss(id);
		uint8_t iid;
		iss >> iid;
		uint8_t indi = 0xee;//1110 111x
		bf.write(indi);
		bf.add(7);
		bf.write(uint8_t(iid << 6));
		bf.add(2);
	}
	else if (nodename == "riichi1")
	{
		uint8_t indi = 0xf0;//1111 00xx
		bf.write(indi);
		bf.add(6);
	}
	else if (nodename == "riichi2")
	{
		uint8_t indi = 0xf4;//1111 01xx
		bf.write(indi);
		bf.add(6);
	}
	else if (nodename == "hu")
	{
		if (ingame)
		{
			const std::string id = node_element->get_attribute_value("id");
			istringstream iss(id);
			uint8_t iid;
			iss >> iid;
			uint8_t indi = 0xc0;//1100 0xxx
			bf.write(indi);
			bf.add(5);
			bf.write(uint8_t(iid << 6));
			bf.add(2);
		}
		else
		{
			const std::string id = node_element->get_attribute_value("id");
			istringstream iss1(id);
			uint8_t iid;
			iss1 >> iid;
			const std::string from = node_element->get_attribute_value("from");
			istringstream iss2(from);
			uint8_t ifrom;
			iss2 >> ifrom;
			uint8_t indi;
			if (iid == ifrom)
			{
				indi = 0x0;//00xx xxxx
				bf.write(indi);
				bf.add(2);
				bf.write(uint8_t(iid << 6));
				bf.add(2);
			}
			else
			{
				indi = 0x40;//01xx xxxx
				bf.write(indi);
				bf.add(2);
				bf.write(uint8_t(iid << 6));
				bf.add(2);
				bf.write(uint8_t(ifrom << 6));
				bf.add(2);
			}
			//score change
			const std::string str = node_element->get_child_text()->get_content();
			istringstream iss(str);
			int16_t s;
			for (int i = 0; i < 4; ++i)
			{
				iss >> s;
				bf.write(uint16_t(s));
				bf.add(16);
			}
			//additional information
			const auto attr = node_element->get_attributes();
			ostringstream oss;
			for (auto it = attr.begin(); it != attr.end(); ++it)
			{
				if (it != attr.begin())
				{
					oss << " ";
				}
				oss << (*it)->get_name() << "=" << (*it)->get_value();
			}
			bf.write_and_add(oss.str());
			bf.write(uint8_t(0));
			bf.add(8);
		}
	}
	else if (nodename == "end")
	{
		ingame = false;
		uint8_t indi = 0xf8;//1111 1xxx
		bf.write(indi);
		bf.add(5);
	}
	else if (nodename == "ryuukyoku")
	{
		uint8_t indi = 0x80;//100x xxxx
		bf.write(indi);
		bf.add(4);
			//score change
			const std::string str = node_element->get_child_text()->get_content();
			istringstream iss(str);
			int16_t s;
			for (int i = 0; i < 4; ++i)
			{
				iss >> s;
				bf.write(uint16_t(s));
				bf.add(16);
			}
			//additional information
			const auto attr = node_element->get_attributes();
			ostringstream oss;
			for (auto it = attr.begin(); it != attr.end(); ++it)
			{
				if (it != attr.begin())
				{
					oss << " ";
				}
				oss << (*it)->get_name() << "=" << (*it)->get_value();
			}
			bf.write_and_add(oss.str());
			bf.write(uint8_t(0));
			bf.add(8);
	}
	const auto node_content = dynamic_cast<const xmlpp::ContentNode*>(node);
	if (!node_content)
	{
		auto list = node->get_children();
		for (auto& child : list)
		{
			process_node(child);
		}
	}

	if (nodename == "game")//end of this game
	{
		uint8_t indi = 0xc0;//11xx xxxx
		bf.write(indi);
		bf.add(2);
	}
}

int main()
{
	xmlpp::DomParser parser;
	parser.parse_file("t1.mjr");
	auto rnode = parser.get_document()->get_root_node();
	bf.set_data(new uint8_t[100000]);
	bf.write_and_add("!mjr");
	process_node(rnode);
	uint8_t indi = 0x00;//0xxx xxxx
	bf.write(indi);
	bf.add(1);

	ofstream ofs("b1.mjr", ios::binary|ios::out);
	ofs.write(reinterpret_cast<char*>(bf.get_data()), bf.size());
	return 0;
}
