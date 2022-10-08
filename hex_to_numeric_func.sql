/*
    01.12.2021
    Данная функция была создана в рамках задачи определения топологии сетевых элементов
    для преобразования hex- в dec-значения ip-адресов соседей сетевых узлов, 
    Используется в материализованном представлении ui_ne_nbrs
*/
create function hex_to_numeric(str text) returns numeric
    immutable
    strict
    language plpgsql
as
$$
declare
    i int;
    n int = length(str)/ 8;
    res dec = 0;
begin
    str := lpad($1, (n+ 1)* 8, '0');
    for i in 0..n loop
        if i > 0 then
            res:= res * 4294967296;
        end if;
        res:= res + concat('x', substr(str, i* 8+ 1, 8))::bit(32)::bigint::dec;
    end loop;
    return res;
end
$$;

alter function hex_to_numeric(text) owner to backend;

 
