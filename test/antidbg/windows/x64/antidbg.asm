
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

prefix_hop_int3 PROC
	db 0f3h,064h,0cch
	ret
prefix_hop_int3 ENDP

kernel_break PROC
	int 02dh
	ret
kernel_break ENDP

END  ; end of the file