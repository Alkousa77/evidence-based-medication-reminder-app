import { Card } from "react-native-paper";
import { PropsWithChildren } from "react";
import { View } from "react-native";

export function AppCard({children}:PropsWithChildren){
    return (

        <Card style={{ padding:10, borderRadius:10, margin:8}}>{children}</Card>

    );
}