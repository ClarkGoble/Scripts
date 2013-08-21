#!/bin/sh
 
# this is the absolute path of the directory you want to process 
# please no trailing slash!
# think twice if it's really necessary to process your entire $HOME
files="/Users/you/Documents"
 
unset a i
while IFS= read -r -d $'\0' file; do
	fileArray[i++]="$file"
done < <(find "$files" -print0)
# echo ${fileArray[@]}
set a i
 
# this is the plist part that will go before and end of tags
plistFront='<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>'
plistEnd='</array></plist>'
 
for currentFile in "${fileArray[@]}"; do
	echo "Processing: $currentFile"
 
	# extract openmeta tags to string
	currentTags=$(/usr/local/bin/openmeta -t -p "$currentFile")
	# remove trailing -p path from openmeta
	currentTags=$(echo ${currentTags%%$currentFile})
	# remove trailing whitespace (if any)
	currentTags=$(echo ${currentTags%%\w})
	
	# only process if there are tags
	if [[ -z $currentTags ]]; then
		echo "File has no tags."
	else
		echo "Number of tags: ${#tagArray[@]}"
		echo "Tags: $currentTags"
		# create array of all tags
		eval tagArray=($currentTags)
	
		# assemble plist string of tags
		plistTagString=""
		for i in "${tagArray[@]}"; do
			# echo "Tag $i"
			plistTagString="$plistTagString<string>$i</string>"
		done
	
		# write tags to file
		xattr -w com.apple.metadata:_kMDItemUserTags "$plistFront$plistTagString$plistEnd" "$currentFile"
	fi
	
	echo	
done
 
# Reading OpenMeta tags:
# xattr -p com.apple.metadata:kMDItemOMUserTags OpenMeta2OSXTags.sh | xxd -r -p | plutil -convert xml1 -o - - | xmllint --xpath "/plist/array/string/text()" -
 
# Writing Mavericks tags
# xattr -w com.apple.metadata:_kMDItemUserTags '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array><string>tag1</string><string>tag2</string></array></plist>'