
import React from "react";
import {View, Text,FlexStyle} from "react-native";
import {AppCard} from "./card";



type Props = {
    title: string;
    subtitle?: string;
    right?: React.ReactNode; //Right item as flex is row
    direction?: FlexStyle["flexDirection"]; //flexdirection type
    bottom?:React.ReactNode;
};


export function ListItem({title, subtitle, right,  direction="row", bottom}:Props){
    return(
        <AppCard>
            <View
            style={{flexDirection: "row", alignItems: "center"}}
            >
                <View style={{flex:1, flexDirection:direction,gap:5}}>
                <Text style={{fontWeight:"600" }}>{title}</Text>
                {subtitle && (
                    <Text style={{color: "black",fontWeight:"600"}}>{subtitle}</Text>
                )}
                </View>             
             {right}   
            </View>
            {bottom && <View style={{marginTop:7}}>{bottom}</View>}
        </AppCard>
    );
}