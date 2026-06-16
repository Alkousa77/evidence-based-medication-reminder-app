import React from "react";
import {View, Text} from "react-native";


type Status = "Taken"|"Missed";

type Props = {
    status: Status;
}

export function StatusBadge({status}:Props){
    const Background = status === "Taken"? "#7cdb5088":status==="Missed"? "#c030306e": "#3d7fdb";
    const color = status === "Taken"? "#2f312e":"#ebe8e8"
    return(
        <View style={{
            minWidth:55,
            alignItems:"center",
            paddingHorizontal:10,
            paddingVertical:4,
            borderRadius:20,
            backgroundColor: Background,
            
        }}>
        <Text style={{fontSize: 12,color:color }}>{status}</Text>
        </View>
    );
}