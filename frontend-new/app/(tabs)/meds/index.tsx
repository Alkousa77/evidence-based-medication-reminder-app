import {FlatList, Text, TouchableOpacity, View} from "react-native";
import {Button} from "react-native-paper";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useCallback, useEffect, useState} from "react";
import api from "@/lib/api";
import { useFocusEffect, useRouter } from "expo-router";
import { AppCard } from "@/components/card";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { ListItem } from "@/components/list-item-card";

export default function MedicationList() {
        const [meds, setMeds] = useState([]);
        const router = useRouter();

        const fetchMeds = async () => {
            try {
                const res = await api.get("/medications");
                setMeds(res.data);
            } catch (error) {
                console.log("failed to fetch meds")
            }
        };

        // fetch meds on focus &(watch funciton passed, any change? rerender)
        useFocusEffect( 
            //save the function (fetch) do not recreate on every render;else focus->fetch->new state(setMed)->new render->new fucntion(because focus watches the function)->loop 
            useCallback(()=>{
            fetchMeds();
        },[])
    );

        const deleteMed = async (id:number) => {
            try {
                await api.delete(`/medications/${id}`)
                //update state of meds
                fetchMeds();
            } catch (error) {
                console.log("failed to delete med")
            }
        };

    return(
        <ScreenWrapper>
        <ScreenHeader title = "Medications" showBackArrow={false}/>
        {/*list*/}
        <FlatList
        data={meds}
        keyExtractor={(item:any)=>item.id.toString()} //KeyExtractor get {id, name, ...} ID is needed as string (to keep track)
        renderItem={({item}: any)=>(                  //renderItem gets {item {id, name, ...}} so destructuring is needed via {item} outputs {id,name,..}   
            <ListItem
            title={item.name}
            subtitle={`${item.amount}${item.dose_unit}`}
            right= {
            <View style={{flexDirection:"row", gap:20, padding:5}}>
            <MaterialIcons name="delete" color="#d14848" size={20} onPress={()=> deleteMed(item.id)}/>
            <MaterialIcons name="edit" size={20} onPress={()=> router.push({pathname: "./meds/edit", params: {medication_id: item.id} })}/> 
            </View>
            }>
            </ListItem>
        )}
        />

        <TouchableOpacity
        onPress={()=>{router.push("./meds/add")}}
        style={{
            position:"absolute", bottom: 20, right: 20, backgroundColor: "#3d7fdb", width:50, height:50, borderRadius: 25, justifyContent:"center", alignItems:"center",
        }}
        >
            <MaterialIcons name="add" size={20} color="white"/>
        </TouchableOpacity>
        </ScreenWrapper>
    )
}