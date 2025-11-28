# Smart Traffic Signal Controller - RISC-V Assembly
# Memory Map:
# 0x1000: Vehicle count sensor (North-South)
# 0x1004: Vehicle count sensor (East-West)
# 0x1008: Emergency override button (0=normal, 1=emergency)
# 0x2000: Traffic light output (NS: bits 0-1, EW: bits 2-3)
#         00=RED, 01=YELLOW, 10=GREEN
# 0x3000: Traffic log memory base

.data
    sensor_ns:    .word 0x1000    # Address of NS sensor
    sensor_ew:    .word 0x1004    # Address of EW sensor
    emergency:    .word 0x1008    # Emergency button address
    light_ctrl:   .word 0x2000    # Traffic light control
    log_base:     .word 0x3000    # Log memory base

.text
.globl main

main:
    # Initialize registers
    addi x10, x0, 0x1000    # x10 = NS sensor address
    addi x11, x0, 0x1004    # x11 = EW sensor address
    addi x12, x0, 0x1008    # x12 = Emergency address
    addi x13, x0, 0x2000    # x13 = Light control address
    addi x14, x0, 0x3000    # x14 = Log base address
    addi x15, x0, 0         # x15 = Log counter

control_loop:
    # Read sensors
    lw x1, 0(x10)           # x1 = NS vehicle count
    lw x2, 0(x11)           # x2 = EW vehicle count
    lw x3, 0(x12)           # x3 = Emergency status
    
    # Check emergency override
    addi x4, x0, 1          # x4 = 1 (emergency check value)
    beq x3, x4, emergency_mode
    
    # Normal operation: Compare traffic density
    blt x1, x2, ew_priority  # If NS < EW, go to EW priority
    jal x0, ns_priority      # Else NS priority

emergency_mode:
    # Set all lights to RED (0b0000 = 0x00)
    addi x5, x0, 0x00       # All RED
    sw x5, 0(x13)           # Write to light control
    jal x0, log_data        # Jump to logging

ns_priority:
    # North-South GREEN, East-West RED (0b0010 = 0x02)
    addi x5, x0, 0x02       # NS=GREEN(10), EW=RED(00)
    sw x5, 0(x13)           # Write to light control
    jal x0, log_data        # Jump to logging

ew_priority:
    # East-West GREEN, North-South RED (0b1000 = 0x08)
    addi x5, x0, 0x08       # NS=RED(00), EW=GREEN(10)
    sw x5, 0(x13)           # Write to light control
    jal x0, log_data        # Jump to logging

log_data:
    # Log traffic snapshot: [NS_count, EW_count, light_state]
    sw x1, 0(x14)           # Store NS count
    sw x2, 4(x14)           # Store EW count
    sw x5, 8(x14)           # Store light state
    addi x14, x14, 12       # Move log pointer forward
    addi x15, x15, 1        # Increment log counter
    jal x0, control_loop    # Return to main loop
