import { Stack } from 'expo-router';
import * as Notifications from "expo-notifications";
import { useEffect } from 'react';
export default function RootLayout() {

  
//set properties for alerts (how notification behaves)
  useEffect(()=>{
    Notifications.setNotificationHandler({
      handleNotification: async () =>({
        shouldShowBanner: true, shouldShowList:true, shouldPlaySound:true,shouldSetBadge:false,
      }),
    });
  },[])


  return (
      <Stack screenOptions = {{headerShown:false}}/>
  );
}