#include "Node.h"

namespace rpc_project_template {

void Node::begin() {
  config_.set_buffer(get_buffer());
  config_.validator_.set_node(*this);
  config_.reset();
  config_.load();
  state_.set_buffer(get_buffer());
  state_.validator_.set_node(*this);
  // Start Serial after loading config to set baud rate.
#if !defined(DISABLE_SERIAL)
  //Serial.begin(config_._.baud_rate);
  /* Hard code baud rate, since configurable baud rate may lead to trouble
   * connecting in the case where the baud rate is initialized to an undefined
   * value. */
  Serial.begin(115200);
#endif  // #ifndef DISABLE_SERIAL
  // Set i2c clock-rate to 400kHz.
  TWBR = 12;
}


void Node::set_i2c_address(uint8_t value) {
  // Validator expects `uint32_t` by reference.
  uint32_t address = value;
  /* Validate address and update the active `Wire` configuration if the
    * address is valid. */
  config_.validator_.i2c_address_(address, config_._.i2c_address);
  config_._.i2c_address = address;
}

}  // namespace rpc_project_template
