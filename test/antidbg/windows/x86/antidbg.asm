.686p
.model flat,C

.code

get_peb_ptr PROC
	;mov eax, dword ptr fs:[030h]
	db 064h,0a1h,030h,00h,00h,00h
	ret
get_peb_ptr ENDP

set_single_step PROC
	pushfd
	or byte ptr[esp+1],1
	popfd
	ret
set_single_step ENDP

set_int3 PROC
	int 3
	ret
set_int3 ENDP


End