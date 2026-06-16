import { PropsWithChildren } from "react";
import { View, StyleSheet } from "react-native";




export function ButtomButtonContainer({children}:PropsWithChildren){
    return (
        <View
        style={styles.container}>
            {children}
        </View>
    );
};

const styles = StyleSheet.create({
    container:{position: "absolute", bottom:0, left:0, right:0 }
}
);