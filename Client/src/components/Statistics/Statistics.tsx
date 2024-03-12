import NavBar from "../NavBar";
import StatStyle from "./Statistics.module.css";

//src/Components/Statistics/Statistics.tsx
function Statistics() {
  return (
    <>
      <div className={StatStyle.container}>
        <div className={StatStyle.navbar}>
          <NavBar />
        </div>
        <div className={StatStyle.searchBar}>
          <h1>Hello</h1>
        </div>
        <div className={StatStyle.chart1}>
          <h1>Hello</h1>
        </div>
        <div className={StatStyle.chart2}>
          <h1>
            Lorem Ipsum is simply dummy text of the printing and typesetting i
          </h1>
        </div>
        <div className={StatStyle.chart3}>
          <h1>
            Lorem Ipsum is simply dummy text of the printing and typesetting
          </h1>
        </div>
      </div>
    </>
  );
}
export default Statistics;
