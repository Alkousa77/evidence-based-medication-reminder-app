import { TextInput } from "react-native-paper";

type  Props = {
    label?: string;
    value: string;
    onChangeText: (Text:string)=> void;
    placeholder?: string;
    secureTextEntry?: boolean;
};

export function AppInput({label, value, onChangeText, placeholder, secureTextEntry}: Props){
    return (
        <TextInput
                label={label}
                value ={value}
                onChangeText={onChangeText}
                placeholder={placeholder}
                secureTextEntry={secureTextEntry}
                mode="outlined"
                dense
                style={{marginBottom:12,}}
                theme= {{roundness:15}}
        ></TextInput>
    );
}
