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
#define Ctrl 0b10000000
#define Alt 0b1000000000000000


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
        default: *GPIO_ODR_HIGH = 0;
	}
}


unsigned short kbdGetCol ( int row, unsigned short Keyb_status){
	unsigned char c;
	
	c = *GPIO_IDR_HIGH;
    
	if ( c & 0x8 ) Keyb_status|= (0b0000000000000001<<((4-row)*4+3));
	if ( c & 0x4 ) Keyb_status|= (0b0000000000000001<<((4-row)*4+2));
	if ( c & 0x2 ) Keyb_status|= (0b0000000000000001<<((4-row)*4+1));
	if ( c & 0x1 ) Keyb_status|= (0b0000000000000001<<((4-row)*4+0));
	return Keyb_status;
}


unsigned short keyb_alt_ctrl(void){
	unsigned short Keyb_status = 0;
	int row, col;
	for (row=1; row <=4 ; row++ ) {
		kbdActivate( row );
		Keyb_status=kbdGetCol (row,Keyb_status);
		kbdActivate( 0 );
		}
	return Keyb_status;
	}



unsigned char key[]={1,2,3,0xA,4,5,6,0xB,7,8,9,0xC,0xE,0,0xF,0xD};

unsigned char keysArray[]={
	0x3F,       
	0x06,
	0x5B,
	0x4F,
	0x66,
	0x6D,
	0x7C,
	0x07,
	0x7F,
	0x67
};



char out7Seg(unsigned char c, int dp){
	if(dp !=0){
		*GPIO_ODR_LOW = (keysArray[c] | 0x80);
	}
    else if(dp ==0){
        *GPIO_ODR_LOW = (keysArray[c]);
    }else{
		*GPIO_ODR_LOW = 0;
	}
}


unsigned char emojiArray[]={
	0b01000000,
	0b01100010, 
	0b01010100, 
	0b01001001,
	0b01011101,
	0b01101011,
};


unsigned char is_numeric( unsigned short s ){
    if (s & 0b0000000000000010) return 0x00; 
    if (s & 0b0001000000000000) return 0x01;
    if (s & 0b0010000000000000) return 0x02;
    if (s & 0b0100000000000000) return 0x03;
    if (s & 0b0000000100000000) return 0x04;
    if (s & 0b0000001000000000) return 0x05;
    if (s & 0b0000010000000000) return 0x06;
    if (s & 0b0000000000010000) return 0x07;
    if (s & 0b0000000000100000) return 0x08;
    if (s & 0b0000000001000000) return 0x09;
    else return 0xFF;
}

void outEmoji(unsigned char c, int dp){
	if(c <6){
        if(dp == 0){
            *GPIO_ODR_LOW = (emojiArray[c]);
        }else{
            *GPIO_ODR_LOW = (emojiArray[c] | 0x80);
		}
	}
    else{
		*GPIO_ODR_LOW = 0b01100100;
	}
}


void main(void)
{
	char t=5;
	unsigned short s;
	unsigned char c;
	int dp;
	app_init();
	
	while(1){
		s = keyb_alt_ctrl();
		dp = s & Alt;
		c = is_numeric(s);
		if(c != 0xFF)
		{
			if(s & Ctrl)
				outEmoji(c,dp);
			else
				out7Seg(c, dp);
		}else
			*GPIO_ODR_LOW = 0;
		}
	}
