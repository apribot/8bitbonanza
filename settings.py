settings = {
'0 saw':{'a': (lambda t : t), 'b': (lambda t: t)},
'1 ANGRY ROBOT':{'a': (lambda t : t*(t<<3|t>>1)), 'b': (lambda t: t*(t<<3+t>>1))},
'2 ARP 7':{'a': (lambda t : (t*1000+t>>106|t*108)/(t+1)), 'b': (lambda t: (t*(7+(1^t>>9%5))))},
'3 BAD GUY THEME':{'a': (lambda t : ((-t&4095)*(1000000&t*(t&t>>10)))), 'b': (lambda t: (1007&t*(904&t>>8&t>>3)>>(3&t>>4)))},
'4 BAGPIPE SAW':{'a': (lambda t : t%118|t%177), 'b': (lambda t: t%118|t%176)},
'5 BIRKIN':{'a': (lambda t : int((t/256)*(t/128))<<69), 'b': (lambda t: (t/128)*(t/16)/2)},
'6 BLINKY LIGHTS':{'a': (lambda t : t*(t<<4&t>>3)), 'b': (lambda t: t*(t<<4&t>>2))},
'7 BOOTSTRAP':{'a': (lambda t : t*((t>>7|t>>5))), 'b': (lambda t: t)},
'8 BOTH WORLDS':{'a': (lambda t : (((t%16)<<6)/8|t%255|t)-12), 'b': (lambda t: ((t%32)<<2)>>2|t%255|(t<<3))},
'9 BROKEN TARDIS':{'a': (lambda t : t^(t>>2)*(t>>7)), 'b': (lambda t: (t*(t>>1|t>>9)))},
'10 CAR ALARM':{'a': (lambda t : (t*((t>>9|t>>13)&15))&128), 'b': (lambda t: ((t+130017)/11091)&(4|t>>96)|(t%16))},
'11 COMPUTING':{'a': (lambda t : (t*(t>>9+t>>9)*100)), 'b': (lambda t: (t*(t>>10+t>>88)*10))},
'12 CONFUSED':{'a': (lambda t : t*t>>11|t>>9), 'b': (lambda t: t*t>>9*((t>>13|t>>41)))},
'13 DATA ERROR':{'a': (lambda t : t*360000*t>>9), 'b': (lambda t: t*30000*t>>11)},
'14 DEFAULT':{'a': (lambda t : t), 'b': (lambda t: t)},
'15 DETUNED ARP':{'a': (lambda t : ((((t>>12)^(t>>12)-2)%29*t)/4|t>>6)), 'b': (lambda t: t)},
'16 EDGY SQUARE':{'a': (lambda t : (t/128)<<7), 'b': (lambda t: (t/32)<<5)},
'17 EFFEM':{'a': (lambda t : ((t*8|t>>3)+139)<<4), 'b': (lambda t: t)},
'18 ELECTROCUTION':{'a': (lambda t : (((t%99)<<6)/4|t%955|t%9999)-12), 'b': (lambda t: ((t%900)|t%999909)-999)},
'19 FOLDBACK WORLD':{'a': (lambda t : (((t%16)<<6)/8|t%255|t)-12), 'b': (lambda t: (((t%16)<<6)/8|t%255|t)-100)},
'20 GAME OVER':{'a': (lambda t : (1000)*t&99999), 'b': (lambda t: 9000&6000%(t+1))},
'21 GEEK LEAD':{'a': (lambda t : (1000)*t&99), 'b': (lambda t: (70000+t)&900+t)},
'22 GEIGER':{'a': (lambda t : t*(t%80|t>>3|t&800)*t), 'b': (lambda t: t)},
'23 GRIT BASS':{'a': (lambda t : (t>>t*t)^t), 'b': (lambda t: t)},
'24 GRUNGY LASER':{'a': (lambda t : (t*t)%(t+100)), 'b': (lambda t: t)},
'25 HAPPY ARP':{'a': (lambda t : t*(t>>9|t>>13)&16), 'b': (lambda t: t)},
'26 HAPPY THEME':{'a': (lambda t : (t*5&t>>6)|(t*3&t>>7)|(t*4&t>>5)), 'b': (lambda t: t)},
'27 HELICOPTER':{'a': (lambda t : (700000+t)&99999900%(t+1)), 'b': (lambda t: t)},
'28 HIDDEN MESSAGE':{'a': (lambda t : t*(t<<1|t>>8)), 'b': (lambda t: t)},
'29 HIGH VOLTAGE':{'a': (lambda t : ((t<<t)|(t>>t))<<4), 'b': (lambda t: t)},
'30 MINOR STAB':{'a': (lambda t : t%50|t%100|t%150|t%200|t%250), 'b': (lambda t: t)},
'31 MOTHERSHIP':{'a': (lambda t : t*(t<<1|t>>8)), 'b': (lambda t: t*(t<<6|t>>8))},
'32 NASTY ARP':{'a': (lambda t : t*t*t*((t>>12|t>>40))&6300), 'b': (lambda t: t*t<<((t>>13|t>>41)))},
'33 NOT QUITE SQUARE':{'a': (lambda t : (t/64)<<6), 'b': (lambda t: t)},
'34 PC LOAD LETTER':{'a': (lambda t : t*360000*t>>9), 'b': (lambda t: t*30000*t>>11)},
'35 PINK DROP':{'a': (lambda t : (1000)*t&99999), 'b': (lambda t: 900&99999900%(t+1))},
'36 POWER SYNTH':{'a': (lambda t : (t%50|t%80)<<4), 'b': (lambda t: t)},
'37 PULSE DIALER':{'a': (lambda t : (((t%99)<<6)/4|t%955|t%9999)-12), 'b': (lambda t: 1/9|t*299982|t%999)},
'38 PWM SAW':{'a': (lambda t : t|t%255), 'b': (lambda t: t|t%252)},
'39 ROBOT SERENADE':{'a': (lambda t : t*((t>>12)|(t>>8))&(63&(t>>4))), 'b': (lambda t: t)},
'40 SAW DROP':{'a': (lambda t : t*(t<<3)/((t-(t<<2))+1)), 'b': (lambda t: t)},
'41 SIMPLE SHIFTY':{'a': (lambda t : t<<2|t>>4), 'b': (lambda t: t)},
'42 SKAROT':{'a': (lambda t : (t^t%127)), 'b': (lambda t: t)},
'43 SQUARE BITS':{'a': (lambda t : (t/128)<<7), 'b': (lambda t: t)},
'44 SQUARE SAW':{'a': (lambda t : (t/128)<<7+t>>2), 'b': (lambda t: t)},
'45 TAKE OFF':{'a': (lambda t : t*t>>10|t/((t&10*t)+1)), 'b': (lambda t: t*40*t)},
'46 TENSION':{'a': (lambda t : (t*2&t*(99&t>>4&t>>9))), 'b': (lambda t: t)},
'47 WAKE UP ALARM':{'a': (lambda t : (t/7&t*(900&t))), 'b': (lambda t: t)},
'48 WALL EE':{'a': (lambda t : t&128|((t*5)&128)), 'b': (lambda t: t&128|((t*7)&128))},
'49 WHISPER':{'a': (lambda t : t*(t<<1|t>>8)), 'b': (lambda t: t*(t<<6|t>>8))},
'50 WURSTBRU':{'a': (lambda t : (t&64)+(t/2)), 'b': (lambda t: t*((t>>12|t>>3)&127&t>>11))}
}