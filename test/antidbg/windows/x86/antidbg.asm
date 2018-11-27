.686p
.model flat,C

.code

get_peb_ptr PROC
	;mov eax, dword ptr fs:[030h]
	db 064h,0a1h,030h,00h,00h,00h
	ret
get_peb_ptr ENDP



End