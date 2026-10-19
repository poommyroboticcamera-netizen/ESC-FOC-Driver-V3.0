/* Temporary bench diagnostic. NO PWM and NO motor commands.
 * STM32F405, HSI 16 MHz, independent ADC1 at 8 MHz.
 * Results at 0x20001000; 3 x 3 x 512 uint16 samples at 0x20002000.
 */
#include <stdint.h>
#define R(a) (*(volatile uint32_t *)(a))
#define GPIOA 0x40020000u
#define GPIOB 0x40020400u
#define GPIOC 0x40020800u
static void delay(unsigned n) { while(n--) __asm volatile("nop"); }
static void mode(unsigned port,unsigned pin,unsigned value) {
    R(port)=(R(port)&~(3u<<(pin*2)))|(value<<(pin*2));
}
static uint16_t sample(unsigned channel) {
    R(0x40012034)=channel; /* SQR3, one conversion */
    R(0x40012008)|=1u<<30;
    unsigned timeout=100000;
    while(!(R(0x40012000)&2u) && --timeout) {}
    return timeout ? (uint16_t)R(0x4001204C) : 0xFFFF;
}
void Reset_Handler(void) {
    __asm volatile("cpsid i");
    R(0xE0042004)|=7u; /* Keep debug accessible in all low-power modes. */
    volatile uint32_t *info=(void*)0x20001000;
    volatile uint16_t (*data)[3][512]=(void*)0x20002000;
    info[0]=0xADC04052;info[1]=0;info[2]=512;info[3]=8000000;
    R(0x40023800)|=1u; while(!(R(0x40023800)&2u)){}
    R(0x40023808)&=~3u;while(R(0x40023808)&12u){}
    R(0x40023830)|=7u; (void)R(0x40023830);
    /* Keep all six driver PWM inputs LOW before enabling the driver. */
    R(GPIOA+0x18)=((1u<<8)|(1u<<9)|(1u<<10))<<16;
    R(GPIOB+0x18)=((1u<<12)|(1u<<13)|(1u<<14)|(1u<<15))<<16;
    for(unsigned p=8;p<=10;p++)mode(GPIOA,p,1);
    for(unsigned p=12;p<=15;p++)mode(GPIOB,p,1);
    mode(GPIOB,0,3);mode(GPIOB,1,3);
    mode(GPIOC,4,1);mode(GPIOC,5,1);
    R(GPIOC+0x18)=((1u<<4)|(1u<<5)|(1u<<10))<<16;
    mode(GPIOC,10,1);mode(GPIOC,12,0);
    R(GPIOC+0x0C)=(R(GPIOC+0x0C)&~(3u<<24))|(1u<<24);
    R(GPIOC+0x18)=1u<<10; /* EN_GATE high, PWM inputs all low. */
    delay(1000000);
    info[4]=R(GPIOC+0x10);
    R(0x40023844)|=1u<<8; (void)R(0x40023844);
    R(0x40012304)=1u<<23; /* independent mode, VREFINT on, PCLK/2 */
    R(0x40012004)=0; /* no scan or interrupts */
    R(0x4001202C)=0;R(0x40012030)=0;
    R(0x4001200C)=7u<<21; /* VREFINT acquisition 480 cycles */
    R(0x40012010)=(1u<<24)|(1u<<27);
    R(0x40012008)=1; /* ADON, software trigger, no DMA */
    delay(100000);
    const unsigned channels[3]={9,8,17};
    for(unsigned profile=0;profile<3;profile++) {
        if(profile==1)R(0x40012010)=(7u<<24)|(7u<<27);
        if(profile==2)R(GPIOB+0x18)=1u<<12; /* DC_CAL internal input short */
        delay(100000);
        for(unsigned i=0;i<512;i++) {
            for(unsigned ch=0;ch<3;ch++)data[profile][ch][i]=sample(channels[ch]);
            delay(100);
        }
        info[1]=profile+1;
    }
    R(GPIOB+0x18)=1u<<28; /* restore DC_CAL LOW */
    info[5]=R(GPIOC+0x10); info[6]=R(GPIOB+0x14);
    info[7]=0x600DC0DE;
    R(GPIOC+0x18)=1u<<4;
    for(;;)__asm volatile("nop"); /* Stay awake for reliable SWD readout. */
}
__attribute__((used,section(".isr_vector")))
void (*const vectors[])(void)={ (void(*)(void))0x20020000,Reset_Handler };
