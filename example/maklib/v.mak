ifeq (${O},)
define OB_MAK_FILE
$(1)
endef
else
define OB_MAK_FILE
	$(shell python ${TOPDIR}/src/obcode_debug.py makob $(1))
endef
endif
#$(1)