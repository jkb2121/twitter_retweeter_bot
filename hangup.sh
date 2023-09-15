#!/bin/bash


STAMP=`date`
echo "Executed hangup2.sh: $STAMP"

TPATH=/home/jkb/code/twitter_retweeter_bot
cd $TPATH

resetfiles() {
    cd $TPATH
    echo "File Reset Function Called in directory: $TPATH"
    mv $TPATH/retweetbot.log.bak $TPATH/retweetbot.log.bak2
    mv $TPATH/retweetbot.log $TPATH/retweetbot.log.bak
    #rm $TPATH/hangup.log
    #touch $TPATH/hangup.log
    
    # rm $TPATH/nohup.out
    # touch $TPATH/nohup.out
    echo "--------------------------------------------" >> $TPATH/nohup.out
    echo "Resetting Twitter Retweeter Bot" >> $TPATH/nohup.out
    date >> $TPATH/nohup.out
    echo "--------------------------------------------" >> $TPATH/nohup.out
    echo "File Reset process complete, returning focus"
}


TPID=`pidof -x threaded_retweeter.py`
echo $TPID
echo $TPID >> $TPATH/nohup.out 
if [ -z "$TPID" ]
    then
        sleep 10 
        TPID=`pidof -x threaded_retweeter.py`
        echo $TPID
        echo "Trying again..." >> $TPATH/nohup.out
        echo $TPID >> $TPATH/nohup.out
fi

if [ -z "$TPID" ]
    then
        echo "Bot is Not Running!"
        echo "Calling Reset!"
        resetfiles
        echo "Reset Files Complete"
        echo "We're in directory: $TPATH"
        sleep 300

        nohup ./threaded_retweeter.py ctcomedybot.yaml &

        mail -s "Threaded Retweeter Bootup" jkb@jkbworld.com <<< 'Booting Threaded Retweeter after finding the system not running--presumably due to a system reboot';
        mail -s "Threaded Retweeter Bootup" ghosty_22@yahoo.com <<< 'Booting Threaded Retweeter after finding the system not running--presumably due to a system reboot';
        echo "Bot Reset is Complete!"
        exit 0
    else
        echo "Bot is Running!"
fi


if /bin/grep -e "Hangup" $TPATH/retweetbot.log
    then 
        echo "Hangup Detected"

        TPID=`pidof -x threaded_retweeter.py`

        echo $TPID
        kill -9 $TPID
        sleep 300

        echo "Resetting Files..."
        resetfiles
        echo "Resetfiles called."

        #mv $TPATH/retweetbot.log $TPATH/retweetbot.log.bak
        #rm $TPATH/hangup.log
        #touch $TPATH/hangup.log
        #rm $TPATH/nohup.out
        #touch $TPATH/nohup.out

        nohup ./threaded_retweeter.py ctcomedybot.yaml &

        mail -s "Threaded Retweeter Hangup Restart" jkb@jkbworld.com <<< 'Restarting Threaded Retweeter due to detected Twitter Hangup';
        mail -s "Threaded Retweeter Hangup Restart" ghosty_22@yahoo.com <<< 'Restarting Threaded Retweeter due to detected Twitter Hangup';
    else 
        echo "No Hangup Detected"
fi







