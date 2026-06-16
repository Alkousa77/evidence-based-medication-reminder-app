import { Button } from "react-native-paper";


type Props = {
    title: string;
    onPress: ()=>void;
    color?: string;
    textColor?: string;
    radius?: number 
}

export function AppButton({title, onPress, color="#3d7fdb", textColor = "white", radius=25}: Props){
    return (
        <Button
        mode="contained"
        onPress={onPress}
        buttonColor={color}
        textColor={textColor}
        style={{margin:10, borderRadius:radius}}
        >{title}</Button>
    );
}

