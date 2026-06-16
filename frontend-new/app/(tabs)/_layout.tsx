import { MaterialIcons } from '@expo/vector-icons';
import { Tabs } from 'expo-router';
import React from 'react';


export default function TabLayout() {
 

  return (
    <Tabs screenOptions={{ headerShown: false, tabBarShowLabel: false}}>
      <Tabs.Screen
        name="home/index"
        options={{
          tabBarIcon: ({color, size})=> <MaterialIcons name="home" color={color} size={size}></MaterialIcons>
        }} />
      <Tabs.Screen
        name="meds"
        options={{
          tabBarIcon: ({color, size})=> <MaterialIcons name="medication" color={color} size={size}></MaterialIcons>
        }} />

      <Tabs.Screen
        name="history/index"
        options={{
          tabBarIcon: ({color, size})=> <MaterialIcons name="history" color={color} size={size}></MaterialIcons>
        }} />

      <Tabs.Screen
        name="Settings"
        options={{
          tabBarIcon: ({color, size})=> <MaterialIcons name="settings" color={color} size={size}></MaterialIcons>
        }}
      
        />
    </Tabs>
  );
}
