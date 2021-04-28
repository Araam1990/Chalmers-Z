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

void init_app ( void )
{
	* ( (unsigned int *) GPIO_MODER) = 0x55005555;
	* ( (unsigned short *) GPIO_OTYPER) = 0x0000;
	* ( (unsigned int *) GPIO_PUPDR ) = 0x00AA0000;
}

void kbdActivate( unsigned int row ){
/* Aktivera angiven rad hos tangentbordet, eller
* deaktivera samtliga*/
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

int kbdGetCol ( row,Keyb_status){
	unsigned char c;
	
	c = *GPIO_IDR_HIGH;
	if ( c & 0x8 ) Keyb_status= Keyb_status + (0b0000000000000001<<((row-1)*4+3));
	if ( c & 0x4 ) Keyb_status= Keyb_status + (0b0000000000000001<<((row-1)*4+2));
	if ( c & 0x2 ) Keyb_status= Keyb_status + (0b0000000000000001<<((row-1)*4+1));
	if ( c & 0x1 ) Keyb_status= Keyb_status + (0b0000000000000001<<((row-1)*4+0));
	return Keyb_status;
}

unsigned short keyb_alt_ctrl(void){
	unsigned int Keyb_status = 0;
	int row, col;
	for (row=1; row <=4 ; row++ ) {
		kbdActivate( row );
		Keyb_status=kbdGetCol (row,Keyb_status);
		kbdActivate( 0 );
		}
	return Keyb_status;
	}
	
	
	//Aktivera rad 4, placera kolumnvärdena i Keyb_status( b0..b3)
	//Aktivera rad 3, lägg till kolumnvärdena i Keyb_status( b4..b7)
	//Aktivera rad 2, lägg till kolumnvärdena i Keyb_status( b8..b11)
	//Aktivera rad 1, lägg till kolumnvärdena i Keyb_status( b12..b14)
	//returnera Keyb_status
	

unsigned char key[]={1,2,3,0xA,4,5,6,0xB,7,8,9,0xC,0xE,0,0xF,0xD};

unsigned char is_numeric( int s ){
	int bins[16]={0};
	int i=0;
	while(s>0)
		{
		bins[i]= s % 2;
		s=s/2;
		i=i+1;
		}
	if (bins[13]==1) return 0;
	if (bins[0]==1) return 1;
	if (bins[1]==1) return 2;
	if (bins[2]==1) return 3;
	if (bins[4]==1) return 4;
	if (bins[5]==1) return 5;
	if (bins[6]==1) return 6;
	if (bins[8]==1) return 7;
	if (bins[9]==1) return 8;
	if (bins[10]==1) return 9;	


	return 0xff;
	}

unsigned char keys[]={
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

char out7seg(char bin){
				*GPIO_ODR_LOW = keys[bin];
				
}

void main(void){
	unsigned short s;
	unsigned char c;
	init_app();

	while( 1 )
	{
		s = keyb_alt_ctrl();
		c = is_numeric( s );
		if( c != 0xFF ){
			out7seg( c );
		}
	}
} 