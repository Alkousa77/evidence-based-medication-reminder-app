import { View, Text, StyleSheet, TouchableOpacity} from "react-native";
import {ReactNode} from "react";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import {useRouter } from "expo-router";


type Props = {
    title: string;
    showBackArrow?:boolean;
}

export default function ScreenHeader({title, showBackArrow=true}: Props){
    const router = useRouter();
    return(
            <View style= {styles.container}>
                {showBackArrow && (
                    <TouchableOpacity
                    onPress={()=>router.back()}>
                        <MaterialIcons  name="arrow-back" size={22} />
                    </TouchableOpacity>
                )}
                <Text style = {styles.title}>{title}</Text>
            </View>
    );
}

const styles = StyleSheet.create({
    container: {
        marginBottom: 8,
        borderBottomWidth:1,
        gap:4,
        padding:10,
        borderBottomColor:"#9e9e9e",
    },
    title: {
        fontSize: 24,
        fontWeight: "600",
    },
});