import {View, Text, TextInput, Button, FlatList, TouchableOpacity} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";
import { useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { ListItem } from "@/components/list-item-card";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";


type Habit = {id:number, name:string, time:string};

export default function Habits(){
    const [habits, setHabits] = useState<Habit[]>([]); 
    const router = useRouter();

    //fetch
    const fetchHabits = async () =>{
        try {

             const res = await api.get("/habits");
             setHabits(res.data);
        } catch (error) {
            console.log("error fetching habits")
        }
    };

    useEffect(()=>{
        fetchHabits();
    },[]);


    const deleteHabit = async (id:number) => {
        try {
            await api.delete(`/habits/${id}`)
            fetchHabits();
        } catch (error) {
            console.log("failed to delete habit");
        }
    };

    return(
        <ScreenWrapper>
        <ScreenHeader title="My Habits"></ScreenHeader>

        {/*List*/}
        <FlatList
        data={habits}
        keyExtractor={(item)=> item.id.toString()}
        renderItem={({item}) => (
            <ListItem
            direction="column"
            title={item.name}
            subtitle={`Time: ${item.time}`}
            right={
            <View style={{flexDirection:"row", gap:20, padding:5}}>
           <MaterialIcons name="delete"
                    size={20}
                    color="#cf4040"
                 onPress={()=>deleteHabit(item.id)}
                
                />
                <MaterialIcons name="edit"
                    size={20}
                    color="#838383"
                 onPress={()=>{router.push({pathname:"/(tabs)/Settings/habit/edit_habit" , params: {habit_id: item.id}})}}/>
                </View>
            }
            />
        )}
        />
        
        <TouchableOpacity
        onPress={()=>{router.push("/(tabs)/Settings/habit/add_habit")}}
        style={{
            position:"absolute", bottom: 20, right: 20, backgroundColor: "#3d7fdb", width:50, height:50, borderRadius: 25, justifyContent:"center", alignItems:"center",
        }}
        >
            <MaterialIcons name="add" size={20} color="white"/>
        </TouchableOpacity>
        </ScreenWrapper>
    )
};

