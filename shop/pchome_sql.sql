desc pchome;

select * from pchome;

select * from pchome where prod_id = 'DMAL8K-A9009LM3P';
select * from pchome where prod_name = '';
select ifnull(prode_id, 1) from pchome;


select prod_id from pchome;
create table temp as (select distinct * from pchome);
select * from pchome;
delete from pchome where prod_id = 'DMAL8K-A9009LM3P';
select * from pchome where prod_name like '%LED時鐘';

set sql_safe_updates=0;
delete from pchome;
select * from pchome;

