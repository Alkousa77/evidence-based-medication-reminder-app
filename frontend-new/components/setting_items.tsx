import React from "react";
import { View, Text } from "react-native";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { Card } from "react-native-paper";

type Props = {
    title: string;
    onPress: ()=>void;}

export function SettingsItems({title, onPress}:Props){
    
    
    return(
            <Card style={{margin: 6}} onPress={onPress}>
                <View style={{padding:16, flexDirection:"row", justifyContent: "space-between", alignItems:"center"}}>
                    <Text style={{fontSize:16}}>{title}</Text>
                    <MaterialIcons name="chevron-right" size={20} />
                </View>
            </Card>
    )
}