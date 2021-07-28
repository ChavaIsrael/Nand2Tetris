// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INFINITELOOP)
    @SCREEN
    D=A;
    @screenAddress
    M=D;

    @KBD
    D=M;

    @BLACK //if any key is pressed
    D;JNE
    
    (WHITE)
        @whiteOrBlack //input to screen
        M=0; 

        (LOOP)//draw teh screen
        @256
        D=A;
        @i
        M=D;

        (LOOPI) //columns
            @32
            D=A;
            @j
            M=D;

            (LOOPJ) //rows
                @whiteOrBlack
                D=M;
                @screenAddress
                A=M; 
                M=D;

                @screenAddress
                M=M+1;

                @j
                M=M-1;
                D=M;
                
                @LOOPJ
                D;JGT

            @i
            M=M-1;
            D=M;

            @LOOPI
            D;JGT

    @INFINITELOOP
    0;JMP        
    

    (BLACK)
        @whiteOrBlack
        M=-1; 
        @LOOP
        0;JMP
        
(END)
@END
0;JMP