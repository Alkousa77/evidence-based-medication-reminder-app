import {SafeAreaView} from "react-native-safe-area-context";
import {View} from "react-native";
import {ReactNode} from "react";
type Props = {
    children: ReactNode;
}

export default function ScreenWrapper({children}:Props){
    return(
        <SafeAreaView style={{flex:1}}>
            <View style= {{padding: 20, flex: 1}}>
                {children}
            </View>
        </SafeAreaView>
    );
}