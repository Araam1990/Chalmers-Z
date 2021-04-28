/*
 * 	startup.c
 *
 */
 
#define GPIO_D 0x40020C00
#define GPIO_MODER ((volatile unsigned int *) (GPIO_D))
#define GPIO_OTYPER ((volatile unsigned short *) (GPIO_D+0x4))
#define GPIO_PUPDR ((volatile unsigned int *) (GPIO_D+0xC))
#define GPIO_IDR_LOW ((volatile unsigned char *) (GPIO_D+0x10))
#define GPIO_IDR_HIGH ((volatile unsigned char *) (GPIO_D+0x11))
#define GPIO_ODR_LOW ((volatile unsigned char *) (GPIO_D+0x14))
#define GPIO_ODR_HIGH ((volatile unsigned char *) (GPIO_D+0x15))

__attribute__((naked)) __attribute__((section (".start_section")) )

void startup ( void ){
	__asm__ volatile(" LDR R0,=0x2001C000\n");		/* set stack */
	__asm__ volatile(" MOV SP,R0\n");
	__asm__ volatile(" BL main\n");					/* call main */
	__asm__ volatile(".L1: B .L1\n");				/* never return */

}

void app_init ( void )
{
	* ( (unsigned int *) GPIO_MODER) = 0x55005555;
	* ( (unsigned short *) GPIO_OTYPER) = 0x0000;
	* ( (unsigned int *) GPIO_PUPDR ) = 0x00AA0000;
}

void kbdActivate( unsigned int row )
{ /* Aktivera angiven rad hos tangentbordet, eller
* deaktivera samtliga */
	switch( row )
	{
		case 1: *GPIO_ODR_HIGH = 0x10; break;
		case 2: *GPIO_ODR_HIGH = 0x20; break;
		case 3: *GPIO_ODR_HIGH = 0x40; break;
		case 4: *GPIO_ODR_HIGH = 0x80; break;
		case 0: *GPIO_ODR_HIGH = 0x00; break;
	}
}

unsigned char keyb(void)
{
	unsigned char key[]={1,2,3,0xA,4,5,6,0xB,7,8,9,0xC,0xE,0,0xF,0xD};
	int row, col;
	for (row=1; row <=4 ; row++ ) {
		kbdActivate( row );
		if( (col = kbdGetCol () ) ){
			kbdActivate( 0 );
			return key [4*(row-1)+(col-1) ];
		}
	}
	kbdActivate( 0 );
	return 0xFF;
}

int kbdGetCol ( void )
{
	unsigned char c;
	c = *GPIO_IDR_HIGH;
	if ( c & 0x8 ) return 4;
	if ( c & 0x4 ) return 3;
	if ( c & 0x2 ) return 2;
	if ( c & 0x1 ) return 1;
	return 0;
}


char out7Seg(char bin){
	
}

unsigned char emojiArray[]={
	0b01000000,
	0b01100010, 
	0b01010100, 
	0b01001001,
	0b01011101,
	0b01101011,
};


void outEmoji(unsigned char c){
	if(c < 6){
		*GPIO_ODR_LOW = emojiArray[c];
	}else{
		*GPIO_ODR_LOW = 0b01100100;
	}
}

void main(void)
{
	
	app_init();
	
	while(1){
		outEmoji(keyb());
	}
	
	
	
}

