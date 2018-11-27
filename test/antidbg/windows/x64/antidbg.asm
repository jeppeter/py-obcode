
.code

get_peb_ptr PROC
	mov rax , qword ptr gs:[060h]
	ret
get_peb_ptr ENDP

set_single_step PROC
	pushfq
	or byte ptr[esp+1],1
	popfq
	ret
set_single_step ENDP


set_int3 PROC
	int 3
	ret
set_int3 ENDP

END  ; end of the file