#!/bin/bash

# get rid of duplicate apps by reindexing
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -seed -r -domain local -domain system -domain user

# reindex mail
rm $HOME"/Library/Mail/v2/MailData/Envelope Index"
rm $HOME"/Library/Mail/v2/MailData/Envelope Index-shm"
rm $HOME"/Library/Mail/v2/MailData/Envelope Index-wal"

# cleanup downloaded mail attachments (you can always redownload later)

#rm -r "/Users/clarkgoble/Library/Mail Downloads/"

# make Library visible

chflags nohidden $HOME/Library

# clean up my Desktop

mv $HOME/"Desktop/*"  $HOME"/Documents/Temporary Files/"

# repair permissions
# run diskutil list to get the name of your partitions

diskutil repairPermissions disk4
diskutil repairPermissions disk5
diskutil repairPermissions disk6
diskutil repairPermissions disk7s2
diskutil repairPermissions disk8s2
diskutil repairPermissions disk8s3
diskutil repairPermissions disk9s2
diskutil repairPermissions disk9s3
diskutil repairPermissions disk10s2


# clear out caches

rm -r $HOME"/Library/Caches/*"

sudo rm -r /Library/Caches/*




