
.code

get_peb_ptr PROC
	mov rax , qword ptr gs:[060h]
	ret
get_peb_ptr ENDP



END  ; end of the file