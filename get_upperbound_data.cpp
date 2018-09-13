#include <fstream>
#include <iostream>

#include "succinct/mapper.hpp"
#include "binary_freq_collection.hpp"
#include "binary_collection.hpp"
#include "upperbound_data.hpp"
#include "util.hpp"

int main(int argc, const char** argv) {

    using namespace ds2i;

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0]
                  << " <collection basename>"
                  << std::endl;
        return 1;
    }

    std::string input_basename = argv[1];

    binary_collection sizes_coll((input_basename + ".sizes").c_str());
    binary_freq_collection coll(input_basename.c_str());

    upperbound_data<> upperbound_data(sizes_coll.begin()->begin(), coll.num_docs(), coll);
}
